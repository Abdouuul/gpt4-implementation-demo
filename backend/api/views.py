from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
from .models import Style, Context, Language
from pydantic import BaseModel
from AIemailRewrite.settings import OPENAI_API_KEY
import json


def list_languages(request):
    languages = Language.objects.all().order_by('name')
    languages_data = list(languages.values())

    return JsonResponse({
        'languages': languages_data
    })

def list_styles(request):
    styles = Style.objects.all().order_by('name')
    styles_data = list(styles.values('id', 'name'))

    return JsonResponse({
        'styles': styles_data
    })

def list_contexts(request):
    contexts = Context.objects.all().order_by('name')
    contexts_data = list(contexts.values('id', 'name'))

    return JsonResponse({
        'contexts': contexts_data
    })
class EmailItem(BaseModel):
    subject: str
    body: str

class EmailWrittenResponse(BaseModel):
    emails: list[EmailItem]

@csrf_exempt
@require_POST
def handle_email_rewrite(request):
    """ Handle email rewrite request from front end """
    try:
        data = json.loads(request.body)

        language_id = data.get('language_id')
        style_id = data.get('style_id')
        context_id = data.get('context_id')
        email = data.get('email')

        if not all([language_id, style_id, context_id, email]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            language = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            return JsonResponse({'error': 'Language not found'}, status=400)
        
        try:
            style = Style.objects.get(id=style_id)
        except Style.DoesNotExist:
            return JsonResponse({'error': 'Style not found'}, status=400)
        
        try:
            context = Context.objects.get(id=context_id)
        except Context.DoesNotExist:
            return JsonResponse({'error': 'Context not found'}, status=400)
        

        try:
            endpoint = "https://gpt4-mini-mns-project-resource.cognitiveservices.azure.com/"
            model_name = "gpt-4.1-mini"
            api_key = OPENAI_API_KEY
            api_version = "2024-12-01-preview"

            client = AzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                api_key=api_key,
            )

            system_prompt = f"""Tu es un assistant expert en rédaction d'emails. 
            Reformule l'email proposé par l'utilisateur en respectant les consignes présentées ci-dessous: 
            
            ### Consignes :
            * Génère 3 versions de l'email, toujours en respectant le contexte, le style et la langue définis ci-dissous.
            * N'invente pas de nouvelles informations. N'utilise que les données présentes dans l'email fournis.
            * Garde le sens original du message.
            * Langue cible : {language.code}
            * Style : {style.name}
            * Contexte : {context.name}"""

            response = client.chat.completions.parse(
                model=model_name,
                response_format=EmailWrittenResponse,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": email},
                ],
            )

            emails = response.choices[0].message.parsed

            return JsonResponse({**emails.model_dump(), "usage": response.usage.total_tokens})
        except Exception as e:
            print(f'Error accesing the gpt API: {e}')
            return JsonResponse({'error': 'Error accesing the gpt API'}, status=500)

    
    except json.JSONDecodeError:
      print('Error occured when loading the body')
      return JsonResponse({'error': 'Error occured when loading the body'}, status=400)

