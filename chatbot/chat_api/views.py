import re
from django.shortcuts import render
from transformers import pipeline
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chat
from .serializers import ChatSerializer
from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("akhileshav8/symptom-check-april-4")
model = AutoModelForCausalLM.from_pretrained("akhileshav8/symptom-check-april-4")

class ChatView(APIView):
    def post(self, request):
        try:

            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                input_text = serializer.validated_data['text']

                tokenizer = AutoTokenizer.from_pretrained("akhileshav8/symptom-check-april-4")
                inputs = tokenizer(input_text, return_tensors="pt").input_ids
                model = AutoModelForCausalLM.from_pretrained("akhileshav8/symptom-check-april-4")
                outputs = model.generate(inputs, max_new_tokens=50, do_sample=True, top_k=50, top_p=0.95)
                generated_text = str(tokenizer.batch_decode(outputs, skip_special_tokens=True))
                xgenerated_text = str(tokenizer.batch_decode(outputs, skip_special_tokens=True))
                parts = xgenerated_text.split('[ Symptoms ]')
                generated_text = parts[0]
        

            return Response({
                "status": True,
                "message" : "Text generated successfully",
                "body": generated_text
            })
        except:
                return Response({
                    "status": False,
                    "message" : "Text generation failed"
                })
            








# # Create your views here.
# pipe = pipeline("text-generation", model="akhileshav8/symptom-check-april-3")



# class ChatView(APIView):
#     def post(self, request):
#         '''Generate text using the provided input text'''
#         serializer = ChatSerializer(data=request.data)
#         if serializer.is_valid():
#             input_text = serializer.validated_data['text']

#             # Perform text generation using the pipeline
#             generator = pipeline("text-generation")
#             generated_text = generator(input_text, max_length=35, do_sample=False)
#             generated_text = generated_text[0]["generated_text"]
#             generated_text = re.sub(r'\| Symptoms ->.*?\n?', '', generated_text)
#             print(generated_text)

#             return Response({"generated_text": generated_text})
#         else:
#             return Response(serializer.errors, status=400)
