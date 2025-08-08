from PIL import Image  
import os  
  
def create_gif(image_folder, prefix, output_name):  
    images = []  
    for file_name in sorted(os.listdir(image_folder)):  
        if file_name.startswith(prefix):  
            file_path = os.path.join(image_folder, file_name)  
            img = Image.open(file_path).convert("RGBA")  
            images.append(img)  
  
    if images:  
        # 獲取所有圖片的最大寬度和高度  
        max_width = max(img.width for img in images)  
        max_height = max(img.height for img in images)  
  
        # 調整所有圖片的大小並合成到透明背景上  
        new_images = []  
        for img in images:  
            # 創建一個完全透明的背景  
            new_img = Image.new('RGBA', (max_width, max_height), (0, 0, 0, 0))  
            # 計算居中位置
            x_offset = (max_width - img.width) // 2
            y_offset = (max_height - img.height) // 2
            # 將圖片粘貼到背景中間，確保透明度正確處理
            if img.mode == 'RGBA':
                new_img.paste(img, (x_offset, y_offset), img)
            else:
                new_img.paste(img, (x_offset, y_offset))
            new_images.append(new_img)  
  
        new_images[0].save(  
            image_folder+output_name,  
            save_all=True,  
            append_images=new_images[1:],  
            optimize=False,  
            duration=200,  
            loop=0,
            disposal=2  # 添加這行：每一幀後清除背景
        )
        
        # 生成水平翻轉版本
        flipped_images = []
        for img in new_images:
            # 水平翻轉圖片
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_images.append(flipped_img)
        
        # 生成翻轉版本的檔名（在副檔名前加上 -r）
        name_parts = output_name.rsplit('.', 1)
        if len(name_parts) == 2:
            flipped_name = name_parts[0] + '-r.' + name_parts[1]
        else:
            flipped_name = output_name + '-r'
            
        flipped_images[0].save(  
            image_folder+flipped_name,  
            save_all=True,  
            append_images=flipped_images[1:],  
            optimize=False,  
            duration=200,  
            loop=0,
            disposal=2
        )  
  
if __name__ == "__main__":  
    image_folder = "D:\\bobo\\bv_vue\\src\\assets\\pet\\Blue Mushroom\\"  # 替換成你的圖片資料夾路徑  
    create_gif(image_folder, "die", "die.gif")  
    create_gif(image_folder, "stand", "stand.gif")  
    create_gif(image_folder, "move", "move.gif")  
    create_gif(image_folder, "jump", "jump.gif")  
    create_gif(image_folder, "hit", "hit.gif")
    
    # 生成完所有 GIF 後，刪除該資料夾下的所有 PNG 檔案
    print("正在刪除 PNG 檔案...")
    png_count = 0
    for file_name in os.listdir(image_folder):
        if file_name.lower().endswith('.png'):
            file_path = os.path.join(image_folder, file_name)
            try:
                os.remove(file_path)
                png_count += 1
                print(f"已刪除: {file_name}")
            except OSError as e:
                print(f"無法刪除 {file_name}: {e}")
    
    print(f"完成！共刪除了 {png_count} 個 PNG 檔案")  