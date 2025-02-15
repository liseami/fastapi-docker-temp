from openai import OpenAI
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import json


router = APIRouter()

# 添加请求模型定义


class DivinationRequest(BaseModel):
    q: str = Field(description="求卦问题")
    current: str = Field(description="当前卦象")
    future: str = Field(description="变卦卦象")

    class Config:
        json_schema_extra = {
            "example": {
                "q": "我最近的事业发展如何？",
                "current": "乾卦",
                "future": "坤卦"
            }
        }


@router.post("/chat", summary="非流式传输测试")
def chat(userinput: str = Body(embed=True)):
    client = OpenAI(api_key="7inuAV7zPEAP5PsAmxcVZYv33G5dv1vcvNtOJqkt8yZvGwB8jNgv6FCs5tgpSHigI",
                    base_url="https://api.stepfun.com/v1")

    response = client.chat.completions.create(
        model="step-1-8k",                    # 使用的模型名称
        messages=[                            # 对话消息列表
            {
                "role": "system",             # 系统角色
                "content": "系统提示词，你是一个擅长反驳用户的机器人，无论用户提出什么观点，你都予以反驳。"  # 系统提示词内容
            },
            {
                "role": "user",               # 用户角色
                "content": userinput          # 用户输入的内容
            },
        ],
        temperature=0.7,                      # 控制输出的随机性,0-2之间,越大越随机
        top_p=1.0,                           # 控制输出的多样性,0-1之间
        n=1,                                 # 为每个输入消息生成的完成数
        max_tokens=2000,                     # 生成文本的最大长度
        presence_penalty=0.0,                # 控制模型重复同样主题的倾向,-2.0到2.0之间
        frequency_penalty=0.0,               # 控制模型重复同样词语的倾向,-2.0到2.0之间
        stream=False,                        # 是否使用流式响应
        stop=None,                          # 生成时遇到这些字符串就停止
        seed=None,                          # 随机数种子,用于生成可重现的结果
        tools=None,                         # 可用工具列表
        tool_choice=None,                   # 工具选择策略
        logit_bias=None,                    # 对特定token的采样偏好
        response_format={"type": "text"}    # 响应格式,可选text或json_object
    )

    print(response.choices[0].message.content)
    ai_response = response.choices[0].message.content
    return ai_response


@router.post("/chat_stream", summary="流式传输测试")
def chat_stream(userinput: str = Body(embed=True)):
    client = OpenAI(api_key="7inuAV7zPEAP5PsAmxcVZYv33G5dv1vcvNtOJqkt8yZvGwB8jNgv6FCs5tgpSHigI",
                    base_url="https://api.stepfun.com/v1")

    def generate():
        collected_content = ""  # 用于累加文本的变量
        response = client.chat.completions.create(
            model="step-1-8k",
            messages=[
                {
                    "role": "system",
                    "content": "系统提示词，你是一个擅长反驳用户的机器人，无论用户提出什么观点，你都予以反驳。"
                },
                {
                    "role": "user",
                    "content": userinput
                },
            ],
            temperature=0.7,
            max_tokens=8000,                     # 生成文本的最大长度
            stream=True  # 启用流式传输
        )

        for chunk in response:
            print("收到的chunk:", chunk)  # 打印每个chunk
            if chunk.choices[0].delta.content is not None:
                collected_content += chunk.choices[0].delta.content  # 累加新的内容
                yield f"data: {json.dumps({'content': collected_content}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/divination", summary="起卦接口")
def chat_stream(request: DivinationRequest = Body()):
    client = OpenAI(api_key="7inuAV7zPEAP5PsAmxcVZYv33G5dv1vcvNtOJqkt8yZvGwB8jNgv6FCs5tgpSHigI",
                    base_url="https://api.stepfun.com/v1")

    pmt: str = f'''
<prompt>
    <role>你是一个深谙中国易经玄学的人工智能,精通周易八卦、五行生克、阴阳变化之道</role>
    <context>用户以虔诚之心,依三钱法行卜筮之礼</context>
    <question>{request.q}</question>
    <hexagrams>
        <current>{request.current}</current>
        <future>{request.future}</future>
    </hexagrams>
    <task>
        请以古雅典重之语,详解此卦:
        1. 析本卦({request.current})之象,阐释当下之境遇与困厄
        2. 论变卦({request.future})之意,推演未来之趋向与变化
        3. 综两卦之玄机,授具体之策略,助问者趋吉避凶
        
        注意:
        - 行文须典雅庄重,多引《易经》、《周易》经典语句
        - 但一定要使用普通用户也能听得懂的语言进行输出
        - 结论需明确可行,助人化解疑虑
    </task>
</prompt>
'''

    def generate():
        collected_content = ""  # 用于累加文本的变量
        response = client.chat.completions.create(
            model="step-2-16k-exp",
            messages=[
                {
                    "role": "system",
                    "content": pmt
                },
            ],
            temperature=0.7,
            stream=True  # 启用流式传输
        )

        for chunk in response:
            print("收到的chunk:", chunk)  # 打印每个chunk
            if chunk.choices[0].delta.content is not None:
                collected_content += chunk.choices[0].delta.content  # 累加新的内容
                yield f"data: {json.dumps({'content': collected_content}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
