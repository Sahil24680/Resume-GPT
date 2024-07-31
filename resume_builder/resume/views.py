from django.shortcuts import render
from googleapiclient.discovery import build
from django.http import HttpResponse
from .resume_template1 import Header, Work_exp, Work_exp_data, Education_data, Education_data_underneath, Skill, update_document_margins,Mini_title,Line_skip, Refresh_doc
from .resume_template1 import authenticate
from . send_template import share_document as send_to
from. send_template import authenticate as auth
def Main(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        document_id = "1AZyVSk_3INKs2LRXe0vV1GbHWOaVFl54vy1dLE4Avh0"
        email = request.POST.get('email')
        job_1 = request.POST.get('job 1')+ '\n'
        job_2 =request.POST.get('job 2')+ '\n'
        job_3 = request.POST.get('job 3')+ '\n'

        project_1 = request.POST.get('project 1')+ '\n'
        project_2 = request.POST.get("project 2")+ '\n'
        project_3 = request.POST.get('project 3')+ '\n'
        

        
        
        
        # Generate the resume
        generate_resume(document_id, name,job_1,job_2,job_3,project_1,project_2,project_3,email)
        
        # Share the document
        #share_document(document_id, recipient_email)
        
        return HttpResponse(f"Resume generated and shared for {name}.")

    return render(request, 'main.html', {})







def generate_resume(document_id, name,job_1,job_2,job_3,project_1,project_2,project_3,email):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
    update_document_margins(document_id)
    header_id=Header(name,document_id)
    lengthg =  Mini_title(1, 'hello123@gmail.com                                    (xxx)-xxx-xxxx                                                        New York, NY\n',document_id)
   
    w1=Work_exp(lengthg,"work exp",document_id)

    if job_1!="\n":
        work_exp=Work_exp_data(w1,job_1,document_id)
    else:
        work_exp = w1
        

    if job_2 !='\n':
        w2 = Work_exp_data(work_exp,job_2,document_id)
    else: 
        w2=work_exp
    
    if job_3 != '\n':
        w3 = Work_exp_data(w2,job_3,document_id)
    else:
        w3=w2

    if job_1 == '\n' and job_2 == '\n' and job_3 == '\n':
        w3=Line_skip(w1,document_id)





    project_exp= Work_exp(w3,"project exp\n",document_id)



    if project_1 !='\n':
        p1=Work_exp_data(project_exp-1,project_1,document_id)
    else:
        p1= project_exp-1


    if project_2!='\n':
        p2 = Work_exp_data(p1,project_2,document_id)
    else:
        p2 = p1
    
    if project_3 !='\n':
        p3 = Work_exp_data(p2,project_3,document_id)
    else:
        p3=p2

    if project_1 == '\n' and project_2 == '\n' and project_3 == '\n':
        p3=Line_skip(project_exp-1,document_id)

    education=Work_exp(p3,"EDUCATION\n",document_id)
    e1 = Education_data(document_id,15,0,0,0,education-1,"Cuny Hunter College - B.S., Computer Science\n",college_name="Cuny Hunter College ",degree= " - B.S., ", major= " Computer Science")
    e2 = Education_data_underneath(document_id,12,.60,.60,.60,e1,"agust 25 2023 - current                                                                                                                      New York, NY\n")


    
    skills = Work_exp(e2,"SKILL\n",document_id)
    end =Skill(skills-1,document_id)
    #Send(document_id,email)
    Refresh_doc(document_id,header_id)
    


def Send(document_id,email):
        creds = auth()
        service = build("drive", "v3", credentials=creds)
        send_to(document_id,email)
