"""崇祯政务档案库的本地网页服务。

服务仅绑定本机回环地址，用于录入、修改、上传和导出资料。
本文件不会调用 AI 分析模块，也不会执行任何游戏操作。
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import mimetypes
import re
import threading
import uuid
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

from modules.database import JSONDatabase
from modules.knowledge_base import MarkdownKnowledgeBase


PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = PROJECT_ROOT / "web"
UPLOAD_ROOT = PROJECT_ROOT / "uploads"
UPLOAD_INDEX = UPLOAD_ROOT / "index.json"
MAX_REQUEST_BYTES = 12 * 1024 * 1024
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {
    ".json",
    ".md",
    ".txt",
    ".csv",
    ".pdf",
    ".docx",
    ".xlsx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

DATASETS: dict[str, dict[str, Any]] = {
    "history": {
        "filename": "history_records.json",
        "fields": [
            "时间",
            "回合",
            "皇帝状态",
            "天下局势",
            "事件",
            "背景",
            "朝廷事件",
            "皇帝决策",
            "玩家决策",
            "诏书内容",
            "执行结果",
            "后续结果",
            "影响评价",
        ],
        "required": ["时间"],
        "list_fields": [],
    },
    "personnel": {
        "filename": "personnel.json",
        "fields": [
            "姓名",
            "身份",
            "派系",
            "职位",
            "影响力",
            "能力",
            "政治倾向",
            "当前状态",
            "与皇帝关系",
            "风险",
            "简介",
            "历史事件",
        ],
        "required": ["姓名"],
        "list_fields": ["历史事件"],
    },
    "edicts": {
        "filename": "edicts.json",
        "fields": ["时间", "诏书标题", "正文", "执行人", "目标", "结果"],
        "required": ["诏书标题", "正文"],
        "list_fields": [],
    },
    "strategy": {
        "filename": "strategy.json",
        "fields": ["目标", "阶段", "措施", "状态", "进展记录"],
        "required": ["目标"],
        "list_fields": ["措施", "进展记录"],
    },
    "personal_notes": {
        "filename": "personal_notes.json",
        "fields": ["游戏时间", "时间", "标题", "来源", "用途", "内容"],
        "required": ["游戏时间", "内容"],
        "list_fields": [],
    },
    "intelligence": {
        "filename": "intelligence.json",
        "fields": ["分类", "来源", "时间", "内容", "重要等级"],
        "required": ["分类", "内容"],
        "list_fields": [],
    },
}


def infer_upload_metadata(
    filename: str,
    requested_category: str = "",
    requested_timeline: str = "",
) -> tuple[str, str]:
    """只依据文件名补充分类和时间节点，不读取或分析文件正文。"""
    name = Path(filename).stem
    category = requested_category.strip()
    if not category or category == "自动分类":
        category_rules = (
            (("诏书", "诏", "圣旨", "谕旨"), "诏书资料"),
            (("天下大势", "局势", "奏疏"), "天下大势"),
            (("朝政", "纪要", "朝廷", "政务"), "朝政奏报"),
            (("财政", "税赋", "国库", "军饷"), "财政资料"),
            (("战争", "军务", "军情", "辽东", "战报"), "战争资料"),
            (("朝臣", "人物", "官员", "人事"), "人物资料"),
            (("回合", "季度", "皇帝日志"), "回合导出"),
        )
        category = "其他"
        for keywords, candidate in category_rules:
            if any(keyword in name for keyword in keywords):
                category = candidate
                break

    timeline = requested_timeline.strip()
    if not timeline:
        match = re.search(
            r"(天启|崇祯)\s*([一二三四五六七八九十百零〇\d]+)\s*年"
            r"(?:[._\-\s·]*)?(春末|夏末|秋末|冬末|春季|夏季|秋季|冬季|春|夏|秋|冬)?",
            name,
        )
        if match:
            year_number = match.group(2)
            chinese_digits = {
                "0": "零",
                "1": "一",
                "2": "二",
                "3": "三",
                "4": "四",
                "5": "五",
                "6": "六",
                "7": "七",
                "8": "八",
                "9": "九",
            }
            if year_number.isdigit():
                year_number = "".join(chinese_digits[digit] for digit in year_number)
            season = (match.group(3) or "").removesuffix("季")
            timeline = f"{match.group(1)}{year_number}年{season}"
    return category, timeline


def write_json(path: Path, data: Any) -> None:
    """原子写入 JSON，避免保存中断产生半个文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    temporary.replace(path)


def read_upload_index() -> list[dict[str, Any]]:
    if not UPLOAD_INDEX.exists():
        write_json(UPLOAD_INDEX, [])
    try:
        data = json.loads(UPLOAD_INDEX.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as error:
        raise ValueError(f"上传索引格式损坏：{error}") from error
    if not isinstance(data, list):
        raise ValueError("上传索引必须是列表。")
    return data


def write_upload_catalog(uploads: list[dict[str, Any]]) -> Path:
    """按时间节点生成可阅读的上传资料目录，不读取文件正文。"""
    catalog_path = PROJECT_ROOT / "大明档案" / "资料索引" / "上传资料目录.md"
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in uploads:
        timeline = str(item.get("时间节点", "")).strip() or "时间节点未标注"
        grouped.setdefault(timeline, []).append(item)

    lines = [
        "# 上传资料目录",
        "",
        "本目录依据上传元数据生成，只记录文件分类和时间节点，不分析正文。",
    ]
    if not uploads:
        lines.extend(["", "（暂无上传资料）"])
    for timeline, items in grouped.items():
        lines.extend(["", f"## {timeline}", ""])
        for item in items:
            filename = str(item.get("原文件名", "未命名文件")).replace("\n", " ")
            category = str(item.get("资料分类", "其他")).replace("\n", " ")
            uploaded_at = str(item.get("上传时间", "时间未记")).replace("\n", " ")
            note = str(item.get("备注", "")).replace("\n", " ")
            purpose = str(item.get("用途", "诏书参考")).replace("\n", " ")
            lines.append(f"- {filename}")
            lines.append(f"  - 分类：{category}")
            if purpose:
                lines.append(f"  - 用途：{purpose}")
            lines.append(f"  - 上传时间：{uploaded_at}")
            if note:
                lines.append(f"  - 备注：{note}")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with catalog_path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines).rstrip() + "\n")
    return catalog_path


def normalize_record(dataset: str, raw: dict[str, Any]) -> dict[str, Any]:
    if dataset not in DATASETS:
        raise ValueError("未知档案类型。")
    if not isinstance(raw, dict):
        raise ValueError("记录内容必须是对象。")

    definition = DATASETS[dataset]
    normalized: dict[str, Any] = {}
    for field in definition["fields"]:
        value = raw.get(field, [])
        if field in definition["list_fields"]:
            if isinstance(value, str):
                value = [
                    item.strip()
                    for item in value.replace("，", ",").split(",")
                    if item.strip()
                ]
            elif not isinstance(value, list):
                value = []
            normalized[field] = [str(item).strip() for item in value if str(item).strip()]
        else:
            normalized[field] = str(value or "").strip()

    missing = [
        field for field in definition["required"] if not normalized.get(field)
    ]
    if missing:
        raise ValueError("必填字段不能为空：" + "、".join(missing))
    return normalized


def infer_note_title(content: str) -> str:
    for line in content.splitlines():
        line = line.strip()
        if line:
            line = re.sub(r"^[#*\s（一二三四五六七八九十0-9）、.]+", "", line).strip()
            return line[:48] or "个人想法"
    return "个人想法"


def normalize_personal_note(raw: dict[str, Any]) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ValueError("记录内容必须是对象。")
    content = str(raw.get("content", raw.get("内容", ""))).strip()
    if not content:
        raise ValueError("想法内容不能为空。")
    game_time = str(raw.get("game_time", raw.get("游戏时间", ""))).strip()
    if not game_time:
        raise ValueError("当前游戏时间不能为空，请填写如“崇祯二年春”。")
    now = datetime.now().astimezone()
    return {
        "游戏时间": game_time,
        "时间": str(raw.get("时间", "")).strip() or now.strftime("%Y-%m-%d %H:%M"),
        "标题": str(raw.get("标题", "")).strip() or infer_note_title(content),
        "来源": str(raw.get("来源", "")).strip() or "网页直接录入",
        "用途": str(raw.get("用途", "")).strip() or "诏书参考",
        "内容": content,
        "创建时间": now.isoformat(timespec="seconds"),
    }


def flatten_intelligence(data: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for category, items in data.items():
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if isinstance(item, dict):
                records.append({"分类": category, "_index": index, **item})
    return records


class ArchiveHTTPServer(ThreadingHTTPServer):
    """携带数据库和写锁的本地 HTTP 服务。"""

    daemon_threads = True

    def __init__(self, server_address: tuple[str, int]) -> None:
        super().__init__(server_address, ArchiveRequestHandler)
        self.database = JSONDatabase(PROJECT_ROOT / "data")
        self.knowledge_base = MarkdownKnowledgeBase(
            self.database, PROJECT_ROOT / "大明档案"
        )
        self.data_lock = threading.RLock()


class ArchiveRequestHandler(BaseHTTPRequestHandler):
    server: ArchiveHTTPServer
    server_version = "ChongzhenArchive/1.0"

    def log_message(self, format_string: str, *args: Any) -> None:
        print(
            f"[{self.log_date_time_string()}] "
            f"{self.client_address[0]} {format_string % args}"
        )

    def _security_headers(self, content_type: str) -> None:
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'",
        )

    def _send_json(self, data: Any, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._security_headers("application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message: str, status: int) -> None:
        self._send_json({"ok": False, "error": message}, status)

    def _read_json_body(self) -> dict[str, Any]:
        content_type = self.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError("请求必须使用 application/json。")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("Content-Length 无效。") from error
        if length <= 0 or length > MAX_REQUEST_BYTES:
            raise ValueError("请求内容为空或超过 12MB。")
        try:
            body = self.rfile.read(length).decode("utf-8")
            parsed = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("请求 JSON 格式无效。") from error
        if not isinstance(parsed, dict):
            raise ValueError("请求主体必须是 JSON 对象。")
        return parsed

    def _write_origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        port = self.server.server_address[1]
        return origin in {
            f"http://127.0.0.1:{port}",
            f"http://localhost:{port}",
        }

    def _serve_static(self, request_path: str) -> None:
        static_files = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
        }
        entry = static_files.get(request_path)
        if not entry:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        filename, content_type = entry
        path = STATIC_ROOT / filename
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self._security_headers(content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _archive_snapshot(self) -> dict[str, Any]:
        db = self.server.database
        return {
            "history": db.load("history_records.json"),
            "personnel": db.load("personnel.json"),
            "edicts": db.load("edicts.json"),
            "strategy": db.load("strategy.json"),
            "game_state": db.load("game_state.json"),
            "personal_notes": db.load("personal_notes.json"),
            "intelligence": flatten_intelligence(
                db.load("intelligence.json")
            ),
            "uploads": read_upload_index(),
            "schemas": {
                key: {
                    "fields": value["fields"],
                    "required": value["required"],
                    "list_fields": value["list_fields"],
                }
                for key, value in DATASETS.items()
            },
        }

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path == "/api/health":
                self._send_json(
                    {
                        "ok": True,
                        "service": "崇祯政务档案库",
                        "analysis_enabled": False,
                    }
                )
                return
            if path == "/api/archive":
                with self.server.data_lock:
                    self._send_json({"ok": True, "data": self._archive_snapshot()})
                return
            if path.startswith("/api/export/"):
                self._export_dataset(unquote(path.removeprefix("/api/export/")))
                return
            if path.startswith("/api/uploads/"):
                self._download_upload(unquote(path.removeprefix("/api/uploads/")))
                return
            self._serve_static(path)
        except ValueError as error:
            self._send_error_json(str(error), HTTPStatus.BAD_REQUEST)
        except OSError as error:
            self._send_error_json(f"文件读取失败：{error}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self) -> None:
        if not self._write_origin_allowed():
            self._send_error_json("拒绝非本地页面的写入请求。", HTTPStatus.FORBIDDEN)
            return
        parsed = urlparse(self.path)
        try:
            payload = self._read_json_body()
            if parsed.path.startswith("/api/records/"):
                dataset = parsed.path.removeprefix("/api/records/")
                self._create_record(dataset, payload)
                return
            if parsed.path == "/api/uploads":
                self._save_upload(payload)
                return
            if parsed.path == "/api/personal-notes":
                self._save_personal_note(payload)
                return
            if parsed.path == "/api/sync-markdown":
                with self.server.data_lock:
                    root = self.server.knowledge_base.sync_all()
                self._send_json({"ok": True, "path": str(root)})
                return
            self._send_error_json("接口不存在。", HTTPStatus.NOT_FOUND)
        except ValueError as error:
            self._send_error_json(str(error), HTTPStatus.BAD_REQUEST)
        except (OSError, binascii.Error) as error:
            self._send_error_json(f"保存失败：{error}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_PUT(self) -> None:
        if not self._write_origin_allowed():
            self._send_error_json("拒绝非本地页面的写入请求。", HTTPStatus.FORBIDDEN)
            return
        parsed = urlparse(self.path)
        match = re.fullmatch(r"/api/records/([a-z]+)/(\d+)", parsed.path)
        if not match:
            self._send_error_json("接口不存在。", HTTPStatus.NOT_FOUND)
            return
        try:
            payload = self._read_json_body()
            query = parse_qs(parsed.query)
            category = query.get("category", [""])[0]
            self._update_record(
                match.group(1), int(match.group(2)), payload, category
            )
        except ValueError as error:
            self._send_error_json(str(error), HTTPStatus.BAD_REQUEST)
        except OSError as error:
            self._send_error_json(f"保存失败：{error}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def _create_record(self, dataset: str, payload: dict[str, Any]) -> None:
        definition = DATASETS.get(dataset)
        if not definition:
            raise ValueError("未知档案类型。")
        record = (
            normalize_personal_note(payload)
            if dataset == "personal_notes"
            else normalize_record(dataset, payload)
        )
        with self.server.data_lock:
            if dataset == "personnel":
                self.server.database.add_person(record)
            elif dataset == "intelligence":
                category = record.pop("分类")
                self.server.database.add_intelligence(category, record)
            else:
                self.server.database.append(definition["filename"], record)
            self.server.knowledge_base.sync_all()
        self._send_json({"ok": True, "message": "档案已保存。"}, HTTPStatus.CREATED)

    def _update_record(
        self,
        dataset: str,
        index: int,
        payload: dict[str, Any],
        category: str,
    ) -> None:
        definition = DATASETS.get(dataset)
        if not definition:
            raise ValueError("未知档案类型。")
        record = (
            normalize_personal_note(payload)
            if dataset == "personal_notes"
            else normalize_record(dataset, payload)
        )

        with self.server.data_lock:
            if dataset == "intelligence":
                intelligence = self.server.database.load("intelligence.json")
                source_category = category or record["分类"]
                if source_category not in intelligence:
                    raise ValueError("原情报分类不存在。")
                if index < 0 or index >= len(intelligence[source_category]):
                    raise ValueError("情报序号无效。")
                target_category = record.pop("分类")
                intelligence[source_category].pop(index)
                intelligence.setdefault(target_category, []).append(record)
                self.server.database.save("intelligence.json", intelligence)
            else:
                records = self.server.database.load(definition["filename"])
                if index < 0 or index >= len(records):
                    raise ValueError("档案序号无效。")
                if dataset == "personnel":
                    new_name = record["姓名"]
                    duplicate = any(
                        item.get("姓名") == new_name and item_index != index
                        for item_index, item in enumerate(records)
                    )
                    if duplicate:
                        raise ValueError(f"人物“{new_name}”已存在。")
                records[index] = record
                self.server.database.save(definition["filename"], records)
            self.server.knowledge_base.sync_all()
        self._send_json({"ok": True, "message": "档案已更新。"})

    def _save_upload(self, payload: dict[str, Any]) -> None:
        original_name = Path(str(payload.get("filename", ""))).name.strip()
        encoded = str(payload.get("content_base64", ""))
        category, timeline = infer_upload_metadata(
            original_name,
            str(payload.get("category", "")),
            str(payload.get("timeline_node", "")),
        )
        note = str(payload.get("note", "")).strip()
        purpose = str(payload.get("purpose", "")).strip() or "诏书参考"
        if not original_name or not encoded:
            raise ValueError("文件名和文件内容不能为空。")
        extension = Path(original_name).suffix.lower()
        if extension not in ALLOWED_UPLOAD_EXTENSIONS:
            allowed = "、".join(sorted(ALLOWED_UPLOAD_EXTENSIONS))
            raise ValueError(f"不支持该文件类型。允许：{allowed}")
        try:
            content = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as error:
            raise ValueError("上传内容不是有效的 Base64。") from error
        if not content or len(content) > MAX_UPLOAD_BYTES:
            raise ValueError("文件为空或超过 10MB。")
        content_hash = hashlib.sha256(content).hexdigest()

        safe_stem = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", Path(original_name).stem)
        safe_stem = safe_stem.strip("._")[:80] or "资料"
        upload_id = uuid.uuid4().hex
        stored_name = f"{upload_id}_{safe_stem}{extension}"
        day_directory = datetime.now().strftime("%Y%m%d")
        relative_path = Path(day_directory) / stored_name
        target = UPLOAD_ROOT / relative_path

        metadata = {
            "id": upload_id,
            "原文件名": original_name,
            "保存路径": relative_path.as_posix(),
            "资料分类": category,
            "时间节点": timeline,
            "用途": purpose,
            "备注": note,
            "上传时间": datetime.now().astimezone().isoformat(timespec="seconds"),
            "文件大小": len(content),
            "内容哈希": content_hash,
        }
        with self.server.data_lock:
            uploads = read_upload_index()
            duplicate = next(
                (
                    item
                    for item in uploads
                    if item.get("内容哈希") == content_hash
                    and item.get("原文件名") == original_name
                ),
                None,
            )
            if duplicate:
                duplicate["资料分类"] = category
                duplicate["时间节点"] = timeline
                duplicate["用途"] = purpose
                if note:
                    duplicate["备注"] = note
                write_json(UPLOAD_INDEX, uploads)
                write_upload_catalog(uploads)
                self._send_json(
                    {
                        "ok": True,
                        "message": "资料已存在，分类和时间节点已更新。",
                        "item": duplicate,
                        "duplicate": True,
                    }
                )
                return
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            uploads.append(metadata)
            write_json(UPLOAD_INDEX, uploads)
            write_upload_catalog(uploads)
        self._send_json(
            {"ok": True, "message": "资料已上传并原样保存。", "item": metadata},
            HTTPStatus.CREATED,
        )

    def _save_personal_note(self, payload: dict[str, Any]) -> None:
        note = normalize_personal_note(payload)
        with self.server.data_lock:
            self.server.database.append("personal_notes.json", note)
            self.server.knowledge_base.sync_all()
        self._send_json(
            {"ok": True, "message": "想法已收录。", "item": note},
            HTTPStatus.CREATED,
        )

    def _download_upload(self, upload_id: str) -> None:
        with self.server.data_lock:
            item = next(
                (entry for entry in read_upload_index() if entry.get("id") == upload_id),
                None,
            )
        if not item:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        relative = Path(str(item["保存路径"]))
        target = (UPLOAD_ROOT / relative).resolve()
        if UPLOAD_ROOT.resolve() not in target.parents or not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = target.read_bytes()
        content_type = mimetypes.guess_type(item["原文件名"])[0]
        self.send_response(HTTPStatus.OK)
        self._security_headers(content_type or "application/octet-stream")
        encoded_name = quote(str(item["原文件名"]))
        self.send_header(
            "Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}"
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _export_dataset(self, dataset: str) -> None:
        definition = DATASETS.get(dataset)
        if not definition:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        data = self.server.database.load(definition["filename"])
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        filename = definition["filename"]
        self.send_response(HTTPStatus.OK)
        self._security_headers("application/json; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="崇祯政务档案库本地网页")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8765, help="监听端口")
    parser.add_argument("--open", action="store_true", help="启动后打开浏览器")
    args = parser.parse_args()

    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("为保护本地档案，本程序只允许绑定 127.0.0.1 或 localhost。")
    if not STATIC_ROOT.exists():
        raise SystemExit(f"前端目录不存在：{STATIC_ROOT}")

    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    uploads = read_upload_index()
    write_upload_catalog(uploads)
    server = ArchiveHTTPServer((args.host, args.port))
    url = f"http://{args.host}:{args.port}"
    print("崇祯政务档案库已启动。")
    print(f"本地地址：{url}")
    print("本页面只负责录入、修改、上传和导出，不执行 AI 分析。")
    print("按 Ctrl+C 停止服务。")

    if args.open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止，已有档案不会被删除。")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
