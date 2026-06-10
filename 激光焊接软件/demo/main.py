"""激光焊接工艺参数查询 - FastAPI后端"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os
from database import init_db, DB_PATH

app = FastAPI(title="激光焊接工艺参数库", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动时初始化数据库
@app.on_event("startup")
def startup():
    init_db()
    print("✅ 数据库已就绪")

# ===== 数据模型 =====
class ParamResult(BaseModel):
    id: int
    material1: str
    material2: str
    thickness: float
    joint_type: str
    speed: float
    power: int
    defocus: str
    shield_gas: str
    gas_flow: float
    fixture: str
    quality: str
    note: str
    is_premium: int
    image_url: str
    video_url: str

class SearchResponse(BaseModel):
    total: int
    results: list[ParamResult]

# ===== API =====

@app.get("/api/search", response_model=SearchResponse)
def search_params(
    material: str = Query("", description="材料搜索关键词"),
    thickness_min: Optional[float] = Query(None),
    thickness_max: Optional[float] = Query(None),
    joint_type: str = Query("", description="接头类型"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    conditions = []
    params = []

    if material:
        conditions.append("(material1 LIKE ? OR material2 LIKE ?)")
        params.extend([f"%{material}%", f"%{material}%"])
    
    if thickness_min is not None:
        conditions.append("thickness >= ?")
        params.append(thickness_min)
    
    if thickness_max is not None:
        conditions.append("thickness <= ?")
        params.append(thickness_max)
    
    if joint_type:
        conditions.append("joint_type LIKE ?")
        params.append(f"%{joint_type}%")

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    # 总数
    c.execute(f"SELECT COUNT(*) FROM weld_params {where}", params)
    total = c.fetchone()[0]

    # 分页
    offset = (page - 1) * page_size
    c.execute(
        f"SELECT * FROM weld_params {where} ORDER BY power LIMIT ? OFFSET ?",
        params + [page_size, offset]
    )
    rows = c.fetchall()
    conn.close()

    results = [dict(r) for r in rows]
    return SearchResponse(total=total, results=results)

@app.get("/api/materials")
def list_materials():
    """获取所有可用的材料列表"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT material1 FROM weld_params 
        UNION 
        SELECT DISTINCT material2 FROM weld_params 
        ORDER BY material1
    """)
    materials = [r[0] for r in c.fetchall()]
    conn.close()
    return {"materials": materials}

@app.get("/api/joint-types")
def list_joint_types():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT joint_type FROM weld_params ORDER BY joint_type")
    types = [r[0] for r in c.fetchall()]
    conn.close()
    return {"joint_types": types}

# ===== 页面 =====
@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=PAGE_HTML)

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>激光焊接工艺参数库</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f6fa; color: #333; }
  .header { background: linear-gradient(135deg, #2F5496 0%, #1a3a6b 100%); color: #fff; padding: 20px 16px; text-align: center; position: sticky; top: 0; z-index: 10; }
  .header h1 { font-size: 20px; font-weight: 600; }
  .header p { font-size: 12px; opacity: 0.8; margin-top: 4px; }
  .container { max-width: 800px; margin: 0 auto; padding: 12px; }
  .search-box { background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  .search-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .search-row input, .search-row select { flex: 1; min-width: 100px; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; outline: none; }
  .search-row input:focus, .search-row select:focus { border-color: #2F5496; }
  .btn-group { display: flex; gap: 8px; margin-top: 10px; }
  .btn { padding: 10px 20px; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; font-weight: 500; }
  .btn-primary { background: #2F5496; color: #fff; flex: 1; }
  .btn-primary:hover { background: #1a3a6b; }
  .btn-outline { background: #fff; color: #666; border: 1px solid #ddd; }
  .btn-outline:hover { background: #f5f5f5; }
  .stats { font-size: 12px; color: #999; margin: 8px 0; }
  .result-card { background: #fff; border-radius: 10px; padding: 14px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-left: 4px solid #2F5496; }
  .result-card.premium { border-left-color: #f0ad4e; }
  .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .result-materials { font-size: 16px; font-weight: 600; color: #2F5496; }
  .result-badge { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #e8f0fe; color: #2F5496; }
  .result-badge.premium { background: #fff3cd; color: #856404; }
  .result-params { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
  .param-item { display: flex; font-size: 13px; padding: 2px 0; }
  .param-label { color: #999; min-width: 60px; }
  .param-value { color: #333; font-weight: 500; }
  .result-note { margin-top: 6px; padding-top: 6px; border-top: 1px solid #eee; font-size: 12px; color: #888; }
  .empty-state { text-align: center; padding: 40px 20px; color: #999; }
  .empty-state .icon { font-size: 48px; margin-bottom: 12px; }
  .loading { text-align: center; padding: 20px; color: #999; display: none; }
  .loading.show { display: block; }
  .footer { text-align: center; padding: 20px; font-size: 11px; color: #bbb; }
  @media (min-width: 600px) {
    .result-params { grid-template-columns: 1fr 1fr 1fr; }
  }
</style>
</head>
<body>

<div class="header">
  <h1>🔧 激光焊接工艺参数库</h1>
  <p>输入材料 → 查询最佳焊接参数</p>
</div>

<div class="container">
  <div class="search-box">
    <div class="search-row">
      <input type="text" id="searchMaterial" placeholder="输入材料名称，如 不锈钢304" autocomplete="off">
      <select id="searchJoint">
        <option value="">全部接头</option>
      </select>
    </div>
    <div class="search-row" style="margin-top:8px">
      <input type="number" id="thicknessMin" placeholder="厚度范围 从(mm)" step="0.5" min="0" style="min-width:80px">
      <input type="number" id="thicknessMax" placeholder="到(mm)" step="0.5" min="0" style="min-width:80px">
    </div>
    <div class="btn-group">
      <button class="btn btn-primary" onclick="search()">🔍 查询参数</button>
      <button class="btn btn-outline" onclick="clearSearch()">清除</button>
    </div>
  </div>

  <div class="stats" id="stats"></div>
  <div class="loading" id="loading">查询中...</div>
  <div id="results"></div>
  <div class="footer">V1.0 Demo · 激光焊接工艺参数库 · 数据持续更新中</div>
</div>

<script>
const API_BASE = '';

// 初始化
async function init() {
  const res = await fetch(`${API_BASE}/api/joint-types`);
  const data = await res.json();
  const sel = document.getElementById('searchJoint');
  data.joint_types.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t;
    sel.appendChild(opt);
  });
  search();
}

let searchTimer = null;
function debounceSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(search, 300);
}

document.getElementById('searchMaterial').addEventListener('input', debounceSearch);
document.getElementById('searchJoint').addEventListener('change', search);
document.getElementById('thicknessMin').addEventListener('input', debounceSearch);
document.getElementById('thicknessMax').addEventListener('input', debounceSearch);

async function search() {
  const material = document.getElementById('searchMaterial').value.trim();
  const joint = document.getElementById('searchJoint').value;
  const tMin = document.getElementById('thicknessMin').value;
  const tMax = document.getElementById('thicknessMax').value;

  document.getElementById('loading').classList.add('show');

  let url = `${API_BASE}/api/search?`;
  if (material) url += `&material=${encodeURIComponent(material)}`;
  if (joint) url += `&joint_type=${encodeURIComponent(joint)}`;
  if (tMin) url += `&thickness_min=${tMin}`;
  if (tMax) url += `&thickness_max=${tMax}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    renderResults(data);
  } catch(e) {
    document.getElementById('results').innerHTML = `<div class="empty-state"><div class="icon">⚠️</div><p>查询失败，请确认服务已启动</p></div>`;
  }
  document.getElementById('loading').classList.remove('show');
}

function renderResults(data) {
  const el = document.getElementById('results');
  const stats = document.getElementById('stats');

  if (data.total === 0) {
    stats.textContent = '';
    el.innerHTML = `<div class="empty-state"><div class="icon">🔍</div><p>未找到匹配参数</p><p style="font-size:12px;margin-top:4px;color:#bbb">试试搜索：不锈钢304 / 碳钢Q235 / 铝合金6061</p></div>`;
    return;
  }

  stats.textContent = `共 ${data.total} 条工艺参数`;
  let html = '';
  data.results.forEach(p => {
    html += `<div class="result-card ${p.is_premium ? 'premium' : ''}">
      <div class="result-header">
        <span class="result-materials">${p.material1} ⟷ ${p.material2}</span>
        <span class="result-badge ${p.is_premium ? 'premium' : ''}">${p.joint_type} · ${p.thickness}mm</span>
      </div>
      <div class="result-params">
        <div class="param-item"><span class="param-label">功率</span><span class="param-value">${p.power} W</span></div>
        <div class="param-item"><span class="param-label">速度</span><span class="param-value">${p.speed} m/min</span></div>
        <div class="param-item"><span class="param-label">离焦量</span><span class="param-value">${p.defocus || '-'}</span></div>
        <div class="param-item"><span class="param-label">保护气</span><span class="param-value">${p.shield_gas || '-'}</span></div>
        <div class="param-item"><span class="param-label">气流量</span><span class="param-value">${p.gas_flow || '-'} L/min</span></div>
        <div class="param-item"><span class="param-label">工装</span><span class="param-value">${p.fixture || '-'}</span></div>
        <div class="param-item"><span class="param-label">质量</span><span class="param-value">${p.quality || '-'}</span></div>
      </div>
      ${p.note ? `<div class="result-note">💡 ${p.note}</div>` : ''}
    </div>`;
  });
  el.innerHTML = html;
}

function clearSearch() {
  document.getElementById('searchMaterial').value = '';
  document.getElementById('searchJoint').value = '';
  document.getElementById('thicknessMin').value = '';
  document.getElementById('thicknessMax').value = '';
  search();
}

// 启动
init();
</script>
</body>
</html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
