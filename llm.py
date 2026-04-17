import requests
from config import ELM_API_URL, ELM_API_KEY, ELM_MODEL


def ask_nuha(user_idea: str, similar_ideas: list) -> str:
    """
    Send the user idea + top similar ideas to Nuha LLM.
    Returns structured Arabic analysis.
    """

    ideas_text = ""
    for i, idea in enumerate(similar_ideas, 1):
        ideas_text += f"{i}. {idea['title']} — {idea['description']} (نسبة التشابه: {idea['score']:.0%})\n"

    prompt = f"""أنت محلل أفكار ابتكارية محترف، ومهمتك تقديم تحليل عملي وواضح باللغة العربية الفصحى المبسطة.

سيصلك:
1) فكرة المستخدم
2) أقرب أفكار مشابهة مع نسب التشابه

قواعد مهمة جداً:
- لا تبالغ في الحكم على الفكرة
- لا تقل إن الفكرة مكررة بالكامل إلا إذا كان التشابه واضحاً جداً
- فرّق بين التشابه في المشكلة، والحل، وآلية التنفيذ
- اجعل اقتراحاتك عملية ومباشرة، وليست عامة
- اكتب بأسلوب واضح ومنظم مناسب للعرض داخل تطبيق

فكرة المستخدم:
{user_idea}

الأفكار الأقرب:
{ideas_text}

أعد الإجابة بهذا التنسيق بالضبط:

التقييم العام:
- اكتب سطراً واحداً يوضح: قريبة جداً / قريبة جزئياً / مختلفة نسبياً

سبب التشابه:
- اكتب 2 إلى 4 نقاط قصيرة

أوجه الاختلاف أو التميز:
- اكتب 2 إلى 3 نقاط قصيرة

اقتراحات التحسين:
- اكتب 3 اقتراحات عملية واضحة"""

    headers = {
        "Authorization": f"Bearer {ELM_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": ELM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = requests.post(ELM_API_URL, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "تعذّر الاتصال بالخادم. تحقق من اتصالك بالإنترنت وحاول مجدداً."
    except requests.exceptions.Timeout:
        return "انتهت مهلة الاتصال. الخادم لا يستجيب حالياً، حاول مجدداً."
    except requests.exceptions.HTTPError as e:
        return f"خطأ من الخادم ({e.response.status_code}). حاول مجدداً لاحقاً."
    except (KeyError, IndexError):
        return "تعذّر قراءة الرد. حاول مجدداً."
