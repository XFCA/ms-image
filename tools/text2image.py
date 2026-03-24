import json,requests,time
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class Text2ImageTool(Tool):
    def __getSize(self,aspect_ratio:str,resolution:int)->str:
        """
        计算图片的宽和高
        """
        aspect_ratio_list = [float(x) for x in aspect_ratio.split(":")]
        if aspect_ratio_list[0] > aspect_ratio_list[1]:
            width = round(resolution*aspect_ratio_list[0]/aspect_ratio_list[1])
            height = resolution
        else:
            width = resolution
            height = round(resolution*aspect_ratio_list[1]/aspect_ratio_list[0])
        return "{0}x{1}".format(width,height)

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        data = [
            ("model",tool_parameters.get("model")),
            ("prompt",tool_parameters.get("prompt")),
            ("negative_prompt",tool_parameters.get("neg_prompt",None)),
            ("size",self.__getSize(tool_parameters.get("aspect_ratio"),tool_parameters.get("resolution"))),
            ("seed",tool_parameters.get("seed",None)),
            ("steps",tool_parameters.get("steps",None)),
            ("guidance",tool_parameters.get("guidance",None)),
            ("loras",tool_parameters.get("loras",None))
        ]

        base_url = 'https://api-inference.modelscope.cn/'
        common_headers = {
            "Authorization": "Bearer "+self.runtime.credentials.get("api_key"),
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({x[0]:x[1] for x in data if x[1] != None}, ensure_ascii=False).encode('utf-8')
        )

        if response.status_code != 200:
            yield self.create_text_message("❌API请求出错，错误码{0}：{1}".format(response.status_code,response.text))
            return
        task_id = response.json()["task_id"]
        response.close()

        waiting = 0
        yield self.create_text_message("⏳图片生成中：")
        while waiting<300:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            if result.status_code != 200:
                yield self.create_text_message("\n❌图片生成失败，错误码{0}：{1}".format(result.status_code,result.text))
                result.close()
                return
            data = result.json()

            if data["task_status"] == "SUCCEED":
                for image_url in data["output_images"]:
                    yield self.create_text_message("\n✔️图片生成成功。")
                    yield self.create_image_message(image_url)
                result.close()
                return
            elif data["task_status"] == "FAILED":
                yield self.create_text_message("\n❌图片生成失败：{0}".format(result.text))
                result.close()
                return
            else:
                time.sleep(5)
                waiting += 5
                yield self.create_text_message(">")

        yield self.create_text_message("\n⏰等待超时。")
        return
