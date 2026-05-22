# LaserWeld Pro - 激光焊接工艺参数查询工具

纯前端Web应用，一键部署到任意静态托管平台。

## 部署方式

### GitHub Pages（推荐）
```bash
# 1. gh auth login（首次需登录GitHub）
gh auth login

# 2. 创建仓库并部署
cd /path/to/project
git init
git add -A
git commit -m "LaserWeld Pro v1.2"
gh repo create laserweld-pro --public --push --source=.
gh repo deploy-key add # 或直接在Settings > Pages中启用
```

### Vercel
```bash
npm install -g vercel
vercel --prod
```

### Cloudflare Pages
在 Cloudflare Dashboard 连接 Git 仓库即可。

## 本地测试
```bash
python3 -m http.server 8080
# 访问 http://localhost:8080
```
