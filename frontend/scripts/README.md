# 图片下载脚本

这个脚本用于下载和优化网站所需的图片资源。

## 功能

- 从 Unsplash 下载图片
- 自动创建所需的目录结构
- 优化图片大小和质量
- 保存为 JPEG 格式

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行脚本：
```bash
python download_images.py
```

## 图片优化说明

- 所有图片会被调整为最大 800x800 像素
- 图片质量设置为 85%
- 使用 JPEG 格式保存
- 启用图片优化

## 目录结构

下载的图片会保存在 `public` 目录下，结构如下：

```
public/
  ├── images/
  │   ├── products/
  │   ├── news/
  │   ├── achievements/
  │   ├── stories/
  │   └── avatars/
```

## 注意事项

- 确保有足够的磁盘空间
- 需要稳定的网络连接
- 如果下载失败，可以重新运行脚本 