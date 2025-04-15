import os
import requests
from PIL import Image
from io import BytesIO

# 图片URL和保存路径映射
IMAGE_MAPPING = {
    # 商品图片
    'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e': '/images/products/product1.jpg',  # 有机大米
    'https://images.unsplash.com/photo-1587486913049-53fc88980cfc': '/images/products/product2.jpg',  # 土鸡蛋
    'https://images.unsplash.com/photo-1587049352851-8d4e89133924': '/images/products/product3.jpg',  # 农家蜂蜜
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/products/product4.jpg',  # 山核桃
    'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f': '/images/products/product5.jpg',  # 农家腊肉
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/products/product6.jpg',  # 野生菌菇
    
    # 商品详情图片
    'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e': '/images/products/detail1.jpg',  # 包装图
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/products/detail2.jpg',  # 使用场景
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/products/detail3.jpg',  # 产地环境
    
    # 扶贫动态图片
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/news/news1.jpg',  # 上线仪式
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/news/news1_1.jpg',  # 丰收场景
    'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e': '/images/news/news2.jpg',  # 培训现场
    
    # 扶贫成果图片
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/achievements/achievement1.jpg',  # 销售现场
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/achievements/achievement2.jpg',  # 培训成果
    'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e': '/images/achievements/achievement3.jpg',  # 电商扶贫
    
    # 扶贫故事图片
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/stories/story1.jpg',  # 致富带头人
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/stories/story2.jpg',  # 返乡创业
    
    # 头像图片
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae': '/images/avatars/avatar1.jpg',  # 农民头像
    'https://images.unsplash.com/photo-1518977676601-b53f82aba655': '/images/avatars/avatar2.jpg',  # 创业者头像
}

def download_and_optimize_image(url, save_path):
    """下载并优化图片"""
    try:
        # 创建目录
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 下载图片
        response = requests.get(url)
        if response.status_code != 200:
            print(f"下载失败: {url}")
            return
        
        # 打开图片
        img = Image.open(BytesIO(response.content))
        
        # 调整图片大小
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 保存图片
        img.save(save_path, 'JPEG', quality=85, optimize=True)
        print(f"下载成功: {save_path}")
        
    except Exception as e:
        print(f"处理图片时出错: {url}, 错误: {str(e)}")

def main():
    # 创建public目录
    os.makedirs('public', exist_ok=True)
    
    # 下载所有图片
    for url, save_path in IMAGE_MAPPING.items():
        full_path = os.path.join('public', save_path.lstrip('/'))
        download_and_optimize_image(url, full_path)

if __name__ == '__main__':
    main() 