"use strict";

const DATASET_LABELS = {
  history: "季度记录",
  personnel: "朝臣档案",
  edicts: "诏书档案",
  strategy: "国策路线",
  personal_notes: "参谋笔记",
  intelligence: "关键情报",
};

const FIELD_HINTS = {
  时间: "如：崇祯元年春",
  游戏时间: "如：崇祯二年春",
  回合: "如：第 1 回合",
  皇帝状态: "健康、威望或其他游戏状态",
  天下局势: "概述本季度全国形势",
  事件: "本季度主要事件",
  背景: "事件发生的背景",
  朝廷事件: "朝堂内的重要事项",
  皇帝决策: "游戏中作出的皇帝决策",
  玩家决策: "玩家的实际选择",
  诏书内容: "本季度相关诏书",
  执行结果: "目前已经看到的结果",
  后续结果: "后续回合再补充",
  影响评价: "由玩家记录影响",
  姓名: "人物姓名",
  身份: "文臣、武将、宗室等",
  派系: "人物所属派系",
  职位: "当前官职",
  影响力: "游戏内影响力数值",
  能力: "擅长领域",
  政治倾向: "政治主张或倾向",
  当前状态: "在任、闲居、下狱等",
  与皇帝关系: "亲近、疏远、待观察等",
  风险: "已知风险，由玩家填写",
  简介: "游戏内人物简介原文，可保留截图截断标记",
  历史事件: "多项请用逗号分隔",
  诏书标题: "诏书名称",
  正文: "完整诏书正文",
  执行人: "负责执行的人或衙门",
  目标: "政策目标或长期目标",
  结果: "尚未发生可留空",
  阶段: "如：1-6 回合",
  措施: "多项请用逗号分隔",
  状态: "未开始、执行中或完成",
  进展记录: "多项请用逗号分隔",
  标题: "可留空，系统会取正文首行",
  来源: "网页录入、上传文件、奏报或玩家补记",
  用途: "如：诏书参考",
  分类: "辽东、陕西、流民、财政、朝堂、外交等",
  内容: "整段原文或情报摘要",
  重要等级: "低、中、高或紧急",
};

const LONG_FIELDS = new Set([
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
  "简介",
  "历史事件",
  "正文",
  "措施",
  "进展记录",
  "内容",
]);

const state = {
  archive: null,
  entryDataset: "history",
  recordDataset: "history",
};

const pageTitles = {
  overview: "档案总览",
  entry: "录入资料",
  records: "查看与修改",
  notes: "录入想法",
  uploads: "上传文件",
};

function element(id) {
  return document.getElementById(id);
}

async function apiRequest(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  let payload;
  try {
    payload = await response.json();
  } catch {
    payload = { ok: false, error: `本地服务返回了无效响应 (${response.status})` };
  }
  if (!response.ok || !payload.ok) {
    throw new Error(payload.error || `请求失败 (${response.status})`);
  }
  return payload;
}

function showGlobalError(message = "") {
  const host = element("global-error");
  host.textContent = message;
  host.hidden = !message;
}

function showToast(message) {
  const toast = element("toast");
  toast.textContent = message;
  toast.hidden = false;
  window.setTimeout(() => {
    toast.hidden = true;
  }, 2600);
}

function setServerState(isOnline, label) {
  const stateHost = document.querySelector(".server-state");
  stateHost.classList.toggle("is-online", isOnline);
  stateHost.classList.toggle("is-offline", !isOnline);
  element("server-label").textContent = label;
}

function showView(viewName) {
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.toggle("is-visible", view.id === `view-${viewName}`);
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === viewName);
  });
  element("page-title").textContent = pageTitles[viewName];
  if (viewName === "records") {
    renderRecordList();
  }
  if (viewName === "uploads") {
    renderUploads();
  }
  if (viewName === "notes") {
    renderNotes();
  }
}

async function refreshArchive() {
  const payload = await apiRequest("/api/archive");
  state.archive = payload.data;
  setServerState(true, "本地服务已连接");
  showGlobalError("");
  renderMetrics();
  renderRecordList();
  renderUploads();
  renderNotes();
}

function renderMetrics() {
  if (!state.archive) {
    return;
  }
  Object.keys(DATASET_LABELS).forEach((dataset) => {
    const target = document.querySelector(`[data-count="${dataset}"]`);
    if (target) {
      target.textContent = String(state.archive[dataset]?.length || 0);
    }
  });
  document.querySelector('[data-count="uploads"]').textContent = String(
    state.archive.uploads?.length || 0,
  );
}

function selectEntryDataset(dataset) {
  state.entryDataset = dataset;
  document.querySelectorAll("[data-dataset]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.dataset === dataset);
  });
  renderArchiveForm(element("entry-form-host"), dataset);
}

function createSelect(field, value) {
  const select = document.createElement("select");
  let options = [];
  if (field === "状态") {
    options = ["", "未开始", "执行中", "完成"];
  } else if (field === "重要等级") {
    options = ["", "低", "中", "高", "紧急"];
  }
  options.forEach((optionValue) => {
    const option = document.createElement("option");
    option.value = optionValue;
    option.textContent = optionValue || "请选择";
    option.selected = optionValue === value;
    select.append(option);
  });
  return select;
}

function createField(field, value, required) {
  const label = document.createElement("label");
  if (LONG_FIELDS.has(field)) {
    label.classList.add("is-wide");
  }

  const labelText = document.createElement("span");
  labelText.textContent = field;
  if (required) {
    const marker = document.createElement("span");
    marker.className = "required";
    marker.textContent = "必填";
    labelText.append(marker);
  }

  let input;
  if (field === "状态" || field === "重要等级") {
    input = createSelect(field, String(value || ""));
  } else if (LONG_FIELDS.has(field)) {
    input = document.createElement("textarea");
    input.value = Array.isArray(value) ? value.join("，") : String(value || "");
  } else {
    input = document.createElement("input");
    input.type = "text";
    input.value = String(value || "");
  }
  input.name = field;
  input.required = required;
  input.placeholder = FIELD_HINTS[field] || "";
  label.append(labelText, input);
  return label;
}

function renderArchiveForm(host, dataset, record = null, editMeta = null) {
  if (!state.archive?.schemas?.[dataset]) {
    host.innerHTML = '<div class="loading-state">正在读取档案字段</div>';
    return;
  }
  host.replaceChildren();
  const schema = state.archive.schemas[dataset];
  const form = document.createElement("form");
  form.className = "archive-form";

  const title = document.createElement("h3");
  title.textContent = editMeta
    ? `修改${DATASET_LABELS[dataset]}`
    : `新增${DATASET_LABELS[dataset]}`;

  const grid = document.createElement("div");
  grid.className = "field-grid";
  schema.fields.forEach((field) => {
    grid.append(
      createField(field, record?.[field], schema.required.includes(field)),
    );
  });

  const actions = document.createElement("div");
  actions.className = "form-actions";
  const submit = document.createElement("button");
  submit.type = "submit";
  submit.className = "button button-primary";
  submit.textContent = editMeta ? "保存修改" : "保存档案";
  const status = document.createElement("p");
  status.className = "form-status";
  actions.append(submit, status);
  form.append(title, grid, actions);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    status.className = "form-status";
    status.textContent = "正在保存";
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    try {
      let path = `/api/records/${dataset}`;
      let method = "POST";
      if (editMeta) {
        method = "PUT";
        path += `/${editMeta.index}`;
        if (dataset === "intelligence") {
          path += `?category=${encodeURIComponent(editMeta.category)}`;
        }
      }
      await apiRequest(path, {
        method,
        body: JSON.stringify(body),
      });
      status.classList.add("is-success");
      status.textContent = editMeta ? "修改已保存" : "档案已保存";
      await refreshArchive();
      if (editMeta) {
        element("edit-dialog").close();
        showToast("档案已更新");
      } else {
        form.reset();
        showToast("档案已保存并同步 Markdown");
      }
    } catch (error) {
      status.classList.add("is-error");
      status.textContent = error.message;
    } finally {
      submit.disabled = false;
    }
  });
  host.append(form);
}

function recordHeading(dataset, record, displayIndex) {
  const candidates = {
    history: [record.时间, record.事件],
    personnel: [record.姓名, record.职位],
    edicts: [record.诏书标题, record.时间],
    strategy: [record.目标, record.状态],
    personal_notes: [record.标题, record.游戏时间, record.时间],
    intelligence: [record.分类, record.时间],
  };
  return candidates[dataset].find(Boolean) || `未命名记录 ${displayIndex + 1}`;
}

function recordSummary(record) {
  const ignored = new Set(["_index"]);
  return Object.entries(record)
    .filter(([key, value]) => !ignored.has(key) && value && String(value).trim())
    .slice(0, 4)
    .map(([key, value]) => {
      const shown = Array.isArray(value) ? value.join("，") : value;
      return `${key}：${shown}`;
    })
    .join("  ");
}

function renderRecordList() {
  const host = element("record-list");
  if (!host) {
    return;
  }
  if (!state.archive) {
    host.innerHTML = '<div class="loading-state">正在读取档案</div>';
    return;
  }
  host.replaceChildren();
  const query = element("record-search").value.trim().toLowerCase();
  const records = state.archive[state.recordDataset] || [];
  const filtered = records
    .map((record, originalIndex) => ({ record, originalIndex }))
    .filter(({ record }) => JSON.stringify(record).toLowerCase().includes(query));

  if (!filtered.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = query
      ? "没有找到符合关键词的档案。"
      : "这一类档案目前为空，可以前往“录入资料”新增。";
    host.append(empty);
    return;
  }

  filtered.forEach(({ record, originalIndex }) => {
    const card = document.createElement("article");
    card.className = "record-card";
    const heading = document.createElement("h3");
    heading.textContent = recordHeading(state.recordDataset, record, originalIndex);
    const summary = document.createElement("p");
    summary.textContent = recordSummary(record);
    const meta = document.createElement("div");
    meta.className = "record-meta";
    meta.textContent = `${DATASET_LABELS[state.recordDataset]} 记录 ${
      originalIndex + 1
    }`;
    const edit = document.createElement("button");
    edit.type = "button";
    edit.className = "button button-secondary";
    edit.textContent = "打开并修改";
    edit.addEventListener("click", () => {
      const dialog = element("edit-dialog");
      element("dialog-title").textContent = recordHeading(
        state.recordDataset,
        record,
        originalIndex,
      );
      renderArchiveForm(
        element("edit-form-host"),
        state.recordDataset,
        record,
        {
          index:
            state.recordDataset === "intelligence"
              ? record._index
              : originalIndex,
          category: record.分类 || "",
        },
      );
      dialog.showModal();
    });
    card.append(heading, summary, meta, edit);
    host.append(card);
  });
}

function formatBytes(bytes) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function renderUploads() {
  const host = element("upload-list");
  if (!host) {
    return;
  }
  host.replaceChildren();
  const uploads = [...(state.archive?.uploads || [])].reverse();
  if (!uploads.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "尚未上传原始资料。";
    host.append(empty);
    return;
  }
  uploads.forEach((item) => {
    const card = document.createElement("article");
    card.className = "upload-item";
    const name = document.createElement("strong");
    name.textContent = item.原文件名;
    const details = document.createElement("p");
    const timeline = item.时间节点 ? `，时间节点：${item.时间节点}` : "";
    const purpose = `，用途：${item.用途 || "诏书参考"}`;
    const notes = item.备注 ? `，${item.备注}` : "";
    details.textContent = `${item.资料分类}，${formatBytes(
      item.文件大小,
    )}${timeline}${purpose}，上传于 ${item.上传时间}${notes}`;
    const link = document.createElement("a");
    link.href = `/api/uploads/${encodeURIComponent(item.id)}`;
    link.textContent = "下载原文件";
    card.append(name, details, link);
    host.append(card);
  });
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const value = String(reader.result);
      resolve(value.slice(value.indexOf(",") + 1));
    };
    reader.onerror = () => reject(new Error("浏览器未能读取该文件。"));
    reader.readAsDataURL(file);
  });
}

function renderNotes() {
  const host = element("note-list");
  if (!host) {
    return;
  }
  host.replaceChildren();
  const notes = [...(state.archive?.personal_notes || [])].reverse();
  if (!notes.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "尚未收录个人想法。";
    host.append(empty);
    return;
  }
  notes.forEach((note) => {
    const card = document.createElement("article");
    card.className = "note-item";
    const title = document.createElement("strong");
    title.textContent = note.标题 || "个人想法";
    const meta = document.createElement("p");
    const gameTime = note.游戏时间 ? `游戏时间：${note.游戏时间}` : "游戏时间：未标注";
    const savedTime = note.时间 ? `收录时间：${note.时间}` : "收录时间未记";
    meta.textContent = `${gameTime}，${savedTime}，${note.用途 || "诏书参考"}，${note.来源 || "网页直接录入"}`;
    const body = document.createElement("div");
    body.className = "note-preview";
    body.textContent = note.内容 || "";
    card.append(title, meta, body);
    host.append(card);
  });
}

async function submitPersonalNote(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const textarea = element("note-content");
  const gameTimeInput = element("note-game-time");
  const status = element("note-status");
  const submit = form.querySelector('button[type="submit"]');
  const content = textarea.value.trim();
  const gameTime = gameTimeInput.value.trim();
  if (!gameTime) {
    status.className = "form-status is-error";
    status.textContent = "请填写当前游戏时间，例如：崇祯二年春。";
    gameTimeInput.focus();
    return;
  }
  if (!content) {
    status.className = "form-status is-error";
    status.textContent = "请先粘贴一整段想法。";
    return;
  }
  submit.disabled = true;
  status.className = "form-status";
  status.textContent = "正在收录";
  try {
    await apiRequest("/api/personal-notes", {
      method: "POST",
      body: JSON.stringify({ game_time: gameTime, content }),
    });
    form.reset();
    status.classList.add("is-success");
    status.textContent = "已收录为参谋笔记，供后续诏书起草读取。";
    await refreshArchive();
    showToast("个人想法已收录");
  } catch (error) {
    status.classList.add("is-error");
    status.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
}

async function submitUpload(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const input = element("upload-file");
  const files = [...input.files];
  const progress = element("upload-progress");
  const submit = form?.querySelector('button[type="submit"]');
  if (!files.length) {
    progress.className = "form-status is-error";
    progress.textContent = "请先选择文件。";
    return;
  }
  const oversized = files.find((file) => file.size > 10 * 1024 * 1024);
  if (oversized) {
    progress.className = "form-status is-error";
    progress.textContent = `${oversized.name} 超过 10MB，未上传。`;
    return;
  }
  if (submit) {
    submit.disabled = true;
  }
  progress.className = "form-status";
  progress.textContent = `正在上传 0/${files.length}`;
  try {
    for (let index = 0; index < files.length; index += 1) {
      const file = files[index];
      progress.textContent = `正在上传 ${index + 1}/${files.length}：${file.name}`;
      const content = await readFileAsBase64(file);
      await apiRequest("/api/uploads", {
        method: "POST",
        body: JSON.stringify({
          filename: file.name,
          content_base64: content,
          category: element("upload-category").value,
          timeline_node: element("upload-timeline").value,
          note: element("upload-note").value,
          purpose: "诏书参考",
        }),
      });
    }
    form.reset();
    element("upload-category").value = "自动分类";
    element("selected-file").textContent = "尚未选择文件";
    progress.classList.add("is-success");
    progress.textContent = `${files.length} 个文件已分类保存，不会触发分析。`;
    await refreshArchive();
    showToast("原始资料已上传");
  } catch (error) {
    progress.classList.add("is-error");
    progress.textContent = error.message;
  } finally {
    if (submit) {
      submit.disabled = false;
    }
  }
}

function setupInteractions() {
  element("upload-category").value = "自动分类";

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => showView(button.dataset.view));
  });
  document.querySelectorAll("[data-go]").forEach((button) => {
    button.addEventListener("click", () => showView(button.dataset.go));
  });
  document.querySelectorAll("[data-quick-dataset]").forEach((button) => {
    button.addEventListener("click", () => {
      selectEntryDataset(button.dataset.quickDataset);
      showView("entry");
    });
  });
  document.querySelectorAll("[data-dataset]").forEach((button) => {
    button.addEventListener("click", () => selectEntryDataset(button.dataset.dataset));
  });

  element("record-dataset").addEventListener("change", (event) => {
    state.recordDataset = event.target.value;
    element("export-link").href = `/api/export/${state.recordDataset}`;
    renderRecordList();
  });
  element("record-search").addEventListener("input", renderRecordList);
  element("note-form").addEventListener("submit", submitPersonalNote);

  element("sync-button").addEventListener("click", async (event) => {
    const button = event.currentTarget;
    const result = element("sync-result");
    button.disabled = true;
    result.textContent = "正在同步";
    try {
      const payload = await apiRequest("/api/sync-markdown", {
        method: "POST",
        body: JSON.stringify({ action: "sync" }),
      });
      result.textContent = `已同步：${payload.path}`;
      showToast("Markdown 知识库已同步");
    } catch (error) {
      result.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });

  element("dialog-close").addEventListener("click", () => {
    element("edit-dialog").close();
  });
  element("edit-dialog").addEventListener("click", (event) => {
    if (event.target === event.currentTarget) {
      event.currentTarget.close();
    }
  });

  const fileInput = element("upload-file");
  fileInput.addEventListener("change", () => {
    const files = [...fileInput.files];
    element("selected-file").textContent = files.length
      ? `已选择 ${files.length} 个文件：${files.map((file) => file.name).join("，")}`
      : "尚未选择文件";
  });
  const dropZone = element("drop-zone");
  ["dragenter", "dragover"].forEach((name) => {
    dropZone.addEventListener(name, (event) => {
      event.preventDefault();
      dropZone.classList.add("is-dragging");
    });
  });
  ["dragleave", "drop"].forEach((name) => {
    dropZone.addEventListener(name, () => {
      dropZone.classList.remove("is-dragging");
    });
  });
  element("upload-form").addEventListener("submit", submitUpload);
}

async function start() {
  setupInteractions();
  renderArchiveForm(element("entry-form-host"), "history");
  try {
    await refreshArchive();
    renderArchiveForm(element("entry-form-host"), "history");
  } catch (error) {
    setServerState(false, "本地服务连接失败");
    showGlobalError(
      `无法读取本地档案：${error.message}。请确认 web_app.py 正在运行。`,
    );
  }
}

document.addEventListener("DOMContentLoaded", start);
