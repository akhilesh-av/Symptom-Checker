from django.shortcuts import render


from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("akhileshav8/symptom-check-april-4")
model = AutoModelForCausalLM.from_pretrained("akhileshav8/symptom-check-april-4")
# Create your views here.
def index(request):
    generated_text = ''
    disease_text = ''
    if request.POST:
        input_text=request.POST['input_text']
        tokenizer = AutoTokenizer.from_pretrained("akhileshav8/symptom-check-april-4")
        inputs = tokenizer(input_text, return_tensors="pt").input_ids
        model = AutoModelForCausalLM.from_pretrained("akhileshav8/symptom-check-april-4")
        outputs = model.generate(inputs, max_new_tokens=60, do_sample=True, top_k=50, top_p=0.95)
        xgenerated_text = str(tokenizer.batch_decode(outputs, skip_special_tokens=True))
        # generated_text = re.sub(r'\ [Symptoms ].*?\n?', '', generated_text)
        parts = xgenerated_text.split('[ Symptoms ]')
        generated_text = parts[0]


        print(generated_text)
        
        index = generated_text.find("[ Disease ]")
        if index != -1:
            disease_text = generated_text[index + len("[ Disease ]"):].strip()
            print(disease_text)

        else:
            disease_text = "No disease found"
        
    return render(request,'index.html',{"content":disease_text})