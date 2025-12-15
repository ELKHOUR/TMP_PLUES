from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json, requests
from fuzzywuzzy import fuzz
from site_app.models import Product, CompanyServices ,CompanyInfo
from .models import CommonQuestion, RawQuestion



#############   PRODUCTS    #################
@csrf_exempt
def chatbot_product(request):
    if request.method != "POST":
        return JsonResponse({"error": "يجب إرسال POST"}, status=400)

    try:
        # قراءة الرسالة المرسلة من المستخدم
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if  user_message == "أريد الاستفسار عن منتج":
            product_url = reverse('home')
            response_text = (
                f"Какой продукт вам нужен ? <br>"
                f"<a href='{product_url}#products' "
                f"style='color:red'>Просмотреть все продукты</a>"
            )
            return JsonResponse({"response": response_text})

        products = Product.objects.all()
        found_product = next(
            (product for product in products if fuzz.partial_ratio(user_message, product.name.lower()) > 70),
            None
        )
        if found_product:
            product_url = reverse('product', args=[found_product.id])
            response_text = (
                f"У нас есть {found_product.name}.<br>"
                f"... {found_product.description[:40]}...<br>"
                f"Цена: {found_product.price}₽.<br>"
                f"<a style='color:red' href='{product_url}'>Посмотреть товар</a>."

            )
        else :
            response_text = f"Не удалось найти товар <span style='color:red'> {user_message} </span>."

        return JsonResponse({"response": response_text})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)








#############   COMPANY INFORMATION    #################
@csrf_exempt
def chatbot_company(request):

    if request.method != "POST":
        return JsonResponse({"error": "يجب إرسال POST"}, status=400)

    try:
        # قراءة الرسالة المرسلة من المستخدم
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if  user_message == "أريد معرفة المزيد عن الشركة":
            return JsonResponse({"response": "Какую информацию вы хотите узнать?"})

        infos = CompanyInfo.objects.all()
        found_info = next(
            (info for info in infos if fuzz.partial_ratio(user_message, info.key.lower()) > 70),
            None
        )
        if found_info:
            response_text = f" удалось найти о компании. <b>{found_info.key}</b>:<br>{found_info.value}"
        else:
            response_text = "Не удалось найти информацию о компании."

        return JsonResponse({"response": response_text})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





#############   SERVES    #################
@csrf_exempt
def chatbot_services(request):

    if request.method != "POST":
        return JsonResponse({"error": "يجب إرسال POST"}, status=400)

    try:
        # قراءة الرسالة المرسلة من المستخدم
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if fuzz.partial_ratio(user_message.lower(), "i want to know this service") > 80:
            return JsonResponse({"response": "О какой услуге вы хотите узнать?"})

        services = CompanyServices.objects.all()
        found_services = next(
            (service for service in services if fuzz.partial_ratio(user_message, service.ServiceName.lower()) > 70),
            None
        )
        if found_services:
            response_text = f"<b>{found_services.ServiceName}</b>:<br>{found_services.ServiceDescription}"
        else:
            response_text = "Этой услуги пока нет. Свяжитесь с нами."

        return JsonResponse({"response": response_text})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



#############   GENERAL SEARCH    #################
@csrf_exempt
def chatbot_general(request):
    if request.method != "POST":
        return JsonResponse({"error": "يجب إرسال POST"}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip().lower()

        # نبحث عن تطابق دقيق أولاً
        exact_match = CommonQuestion.objects.filter(question_text__iexact=user_message).first()
        if exact_match:
            exact_match.repeat_count += 1
            exact_match.save(update_fields=["repeat_count"])
            return JsonResponse({"response": exact_match.answer_text})

        # نبحث عن أقرب سؤال من حيث التشابه
        best_match = None
        best_score = 0

        for q in CommonQuestion.objects.all():
            score = fuzz.partial_ratio(user_message, q.question_text.lower())
            if score > best_score:
                best_score = score
                best_match = q

        # نحدد عتبة التشابه المقبولة
        if best_match and best_score >= 65:
            best_match.repeat_count += 1
            best_match.save(update_fields=["repeat_count"])
            return JsonResponse({
                "response": f"{best_match.answer_text}"
            })

        else:
            return JsonResponse({
                "response": "Извините, я не смог найти подходящий ответ на ваш вопрос 😕. Попробуйте переформулировать его."
            })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



#############   COMMON QUESTION    #################
def search_CommonQuestions(request):
    if request.method == "GET":
        user_message = request.GET.get('q', '').strip().lower()

        if not user_message:
            # لو مفيش نص، ارجع قائمة فارغة
            return JsonResponse({"CommonQuestions": []})

        # جلب كل الأسئلة (يمكن تحسين الأداء لاحقًا)
        all_questions = CommonQuestion.objects.all()

        # البحث بالـ Fuzzy Matching
        matched_questions = [
            {"question_text": q.question_text, "answer_text": q.answer_text}
            for q in all_questions
            if fuzz.partial_ratio(user_message, q.question_text.lower()) > 70
        ]

        # عرض أول 5 أسئلة فقط لتقليل الضغط
        matched_questions = matched_questions[:5]

        # لو ما فيش نتائج، ارجع قائمة فارغة (يمكن عرض الأزرار الافتراضية في الجافاسكريبت)
        return JsonResponse({"CommonQuestions": matched_questions})

    return JsonResponse({"CommonQuestions": []})







#############   save_or_update_question_fuzzy    #################
@csrf_exempt
def save_or_update_question_fuzzy(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # =========================
        # 1️⃣ قراءة الرسالة من الطلب
        # =========================
        data = json.loads(request.body)
        new_question_text = data.get("message", "").strip()

        if not new_question_text:
            return JsonResponse({"error": "Empty question"}, status=400)

        # =========================
        # 2️⃣ استدعاء API الثاني للحصول على الرد
        # =========================
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chatbot/general/",
                json={"message": new_question_text},
                timeout=10
            )
            chatbot_data = response.json()
            chatbot_reply = chatbot_data.get("response", "")
            # تحديد إذا تم الرد أو لا
            isanswered = chatbot_reply != 'Извините, я не смог найти подходящий ответ на ваш вопрос 😕. Попробуйте переформулировать его.'
        except Exception as e:
            chatbot_reply = f"Error calling chatbot_general: {e}"
            isanswered = False

        # =========================
        # 3️⃣ البحث عن أقرب سؤال موجود في قاعدة البيانات
        # =========================
        all_questions = RawQuestion.objects.all()
        closest_question = None
        highest_score = 0

        for q in all_questions:
            score = fuzz.partial_ratio(new_question_text.lower(), q.question_text.lower())
            if score > highest_score:
                highest_score = score
                closest_question = q

        # =========================
        # 4️⃣ تحديد التصرف بناءً على التشابه وعدد مرات السؤال
        # =========================
        if closest_question and highest_score >= 70:
            # تحديث سؤال موجود
            closest_question.count += 1
            closest_question.answered = isanswered
            closest_question.save()

            # لو السؤال تكرر كثيرًا وكان له نفس حالة الإجابة، ننقله إلى CommonQuestion
            if closest_question.count >= 10 and closest_question.answered == isanswered:
                CommonQuestion.objects.create(
                    question_text=closest_question.question_text,
                    answer_text=chatbot_reply
                )
                closest_question.delete()

            question_data = {
                "question_text": closest_question.question_text,
                "count": closest_question.count,
                "answered": closest_question.answered
            }

        else:
            # إنشاء سؤال جديد
            new_q = RawQuestion.objects.create(
                question_text=new_question_text,
                count=1,
                answered=isanswered
            )
            question_data = {
                "question_text": new_q.question_text,
                "count": new_q.count,
                "answered": new_q.answered
            }

        # =========================
        # 5️⃣ إرجاع كل البيانات للـ frontend
        # =========================
        return JsonResponse({
            "status": "success",
            "question": question_data,
            "chatbot_reply": chatbot_reply
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)























