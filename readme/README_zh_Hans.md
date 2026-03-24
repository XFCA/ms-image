
# ModelScope-Image

一个基于 ModelScope API-Inference 的 Dify 插件，提供文生图（Text-to-Image）和图生图（Image-to-Image）功能，支持调用 ModelScope 平台上的大部分 AIGC 模型。

## 功能特性

- **多模型支持**：可调用 ModelScope 平台上绝大多数 AIGC 模型，包括但不限于 `Tongyi-MAI/Z-Image-Turbo`、`MusePublic/489_ckpt_FLUX_1`、`Qwen/Qwen-Image-2512` 等，用户只需在参数中指定模型 ID 即可自由切换。
- **文生图（text2image）**：根据文本提示生成图像，支持正向/负向提示词、宽高比、分辨率、随机种子、采样步数、引导系数等参数调节。
- **图生图（image2image）**：以用户上传的图像为模板，结合文本提示生成新图像，支持与原图相同或自定义的宽高比，以及所有文生图支持的参数。
- **灵活的参数调节**：
  - **宽高比**：提供 7 种常用比例（1:1、4:3、3:4、16:9、9:16、2:1、1:2），图生图还支持“原图”选项。
  - **分辨率**：64 至 2048 范围可调，满足不同清晰度需求。
  - **采样步数**：1 至 100 步，控制生成质量和速度。
  - **引导系数**：1.5 至 20，调节提示词对结果的影响强度。
  - **随机种子**：固定种子可复现生成结果。
  - **LoRA 模型**：支持指定与基础模型兼容的 LoRA 模型 ID，用于风格迁移或细节增强。

## 安装与配置

### 1. 获取 API Key

使用本插件前，你需要从 ModelScope 获取 API Key：

- 访问 [ModelScope Access Token 页面](https://modelscope.cn/my/myaccesstoken)
- 登录你的账号
- 创建或复制你的 API Key（格式通常为 `ms-xxxxxx`）
![API KEY](_assets/api_key.png)

### 2. 在 Dify 中安装插件

将本插件添加到 Dify 的插件目录中，或在 Dify 插件管理界面中安装。

### 3. 配置 API Key

在插件的凭证配置中填入你的 ModelScope API Key。

### 4. （图生图专用）环境变量配置

若使用图生图（image2image）功能，需要在 Dify 的 `.env` 文件中设置内部文件访问 URL，以确保插件能够正确读取用户上传的图像文件：

```bash
INTERNAL_FILES_URL=http://api:5001
```

该配置用于 Dify 内部容器通信，若未设置可能导致图生图工具无法获取输入图像。

## 使用示例

### 文生图

```
model: "Tongyi-MAI/Z-Image-Turbo"
prompt: "a cute cat on sofa"
aspect_ratio: "16:9"
resolution: 1080
```
![text-to-image](_assets/text2image.png)

### 图生图

```
model: "MusePublic/489_ckpt_FLUX_1"
prompt: Turn this picture into an anime style, keeping the content and composition unchanged."
image: [上传的图像文件]
aspect_ratio: "original"
resolution: 1080
loras: "liurui20111959/Ghibli_Style_2"
```
![text-to-image](_assets/image2image.png)

## 开发说明

本插件使用 Python 编写，结构如下：

```
ms-image/
├── manifest.yaml               # 插件元数据
├── main.py                     # 插件启动入口
├── provider/
│   ├── ms-image.yaml           # 提供者配置
│   └── ms-image.py             # 提供者主逻辑
├── tools/
│   ├── text2image.yaml         # 文生图工具定义
│   ├── text2image.py           # 文生图实现
│   ├── image2image.yaml        # 图生图工具定义
│   └── image2image.py          # 图生图实现
├── readme/
│   └── README_zh_Hans.md       # 中文readme
├── README.md                   # 英文 readme
├── PRIVACY.md                  # 隐私协议
└── icon.svg                    # 插件图标
```

- **Python 版本**：3.12
- **支持架构**：amd64, arm64

### 运行入口

插件启动入口为 `main`，定义在 `provider/ms-image.py` 中。

## 注意事项

- 请确保 API Key 具有足够的权限调用对应的模型服务。
- 图生图功能中，输入图像的文件格式建议为常见格式（如 PNG、JPEG），并确保环境变量 `INTERNAL_FILES_URL` 已正确配置。
- 不同模型支持的参数范围和功能可能略有差异，请以 ModelScope 官方文档为准。
- 查看[ModelScope可免费使用AIGC模型](https://www.modelscope.cn/models?filter=inference_type&page=1&tabKey=task&tasks=hotTask:text-to-image-synthesis&type=tasks)。

## 隐私与许可

- 隐私说明详见 [PRIVACY.md](./PRIVACY.md)
- 本插件遵循 ModelScope API 的使用条款

## 作者

- **jinhaow**

## 版本

当前版本：`0.0.1`
