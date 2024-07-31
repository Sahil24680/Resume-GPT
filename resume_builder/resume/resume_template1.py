import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token1.json'):
        creds = Credentials.from_authorized_user_file('token1.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token1.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def Refresh_doc(document_id,header_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=document_id).execute()
    end_index = document['body']['content'][-1]['endIndex']
    

    

    requests = [
                {
        "deleteHeader": {
            "headerId": header_id,
        }
        },
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': end_index -1,
                }

            }

        },

    ]




    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    

def update_document_margins(document_id ):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)

    requests = [
        {
            'updateDocumentStyle': {
                'documentStyle': {


                    
                    'marginLeft': {
                        'magnitude': 25 ,
                        'unit': 'PT'
                    },
                    'marginRight': {
                        'magnitude': 25,
                        'unit': 'PT'
                    },
                   
                },
                'fields': 'marginLeft,marginRight'
            }
        }
    ]

    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()











def Header(text,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
     # Create a header
    requests = [
        {
      "createHeader": {
        "type": 'DEFAULT'
      }
      
    },
    ]

    # Execute the createHeader request to get the header ID
    response = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    header_id = response['replies'][0]['createHeader']['headerId']

    # Define the text to be inserted into the header and the document body

    header_length = len(text)
    requests = [
        # Insert text into the header
        {
            'insertText': {
                'location': {
                    'segmentId': header_id,
                    'index': 0
                },
                'text': text
            }
        },
        # Style the header text
        {
            'updateTextStyle': {
                'range': {
                    'segmentId': header_id,
                    'startIndex': 0,
                    'endIndex': header_length,
                },
                'textStyle': {
                    'bold': True,
                     'weightedFontFamily': {
                    'fontFamily': 'Spectral'
                },
                    'fontSize': {
                        'magnitude': 40,
                        'unit': 'PT'
                    },
                    'underline': False
                },
                'fields': 'bold,fontSize,underline,weightedFontFamily'
            }
        },
        # Align the header text to the left
        {
            'updateParagraphStyle': {
                'range': {
                    'segmentId': header_id,
                    'startIndex': 0,
                    'endIndex': header_length,
                },
                'paragraphStyle': {
                    'alignment': 'CENTER',
                    'indentStart': {
                        'magnitude': 0,  # Ensure no indentation from the left margin
                        'unit': 'PT'
                    },
                    'indentEnd': {
                        'magnitude': 0,  # Ensure no indentation from the right margin
                        'unit': 'PT'
                    }
                },
                'fields': 'alignment,indentStart,indentEnd'
            }
        },
     ]
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return header_id
    


def insert_section_break( start_index,type,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
    requests = [
        {
            'insertSectionBreak': {
                'sectionType': type,  # 'NEXT_PAGE' or 'CONTINUOUS'
                'location': {
                    'index': start_index
                }
            }
        }
    ]
    
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return result



def Insert_img(img,index):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
    
    # Create a request to insert the image
    requests = [
        {
            'insertInlineImage': {
                'location': {
                    'index': index
                },
                'uri': img,
                'objectSize': {
                    'height': {
                        'magnitude': 50,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': 35,
                        'unit': 'PT'
                    }
                }
            }
            
        }

    ]
    
    # Execute the request
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return result

def Line_skip(index,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    requests = [
    # Insert normal content into the document body
    {
        'insertText': {
            'location': {
                'index': index,  # Insert right after the header
            },
            'text': '\n'
        }
    },
      ]
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return(index+1)

def Education_data_underneath(document_id,font,r,g,b,index,text):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    requests = [
    # Insert normal content into the document body
    {
        'insertText': {
            'location': {
                'index': index,  # Insert right after the header
            },
            'text': text
        }
    },
    
    
    
    # Style the content text
    {
        'updateTextStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + len(text) # Ensure this covers the content_text range
            },
            'textStyle': {
                'bold': True,
                'weightedFontFamily': {
                    'fontFamily': 'Spectral'
                },
                'fontSize': {
                    'magnitude': font,
                    'unit': 'PT'
                },
                'underline': False,
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'red': r,
                                'green': g,
                                'blue': b
                            }
                        }
                    }
                
            },
            'fields': 'bold,weightedFontFamily,fontSize,underline,foregroundColor'
        }
    },
    
 
    # Left align the content text
    
   
]
    

    # Execute the requests to insert and style the text
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return(index + len(text))
    



def Education_data(document_id,font,r,g,b,index,text,college_name,degree, major):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    requests = [
    # Insert normal content into the document body
    {
        'insertText': {
            'location': {
                'index': index,  # Insert right after the header
            },
            'text': text
        }
    },
    
    
    
    # Style the content text
    {
        'updateTextStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + len(college_name) # Ensure this covers the content_text range
            },
            'textStyle': {
                'bold': True,
                'weightedFontFamily': {
                    'fontFamily': 'Spectral'
                },
                'fontSize': {
                    'magnitude': font,
                    'unit': 'PT'
                },
                'underline': False,
                    'foregroundColor': {
                        'color': {
                            'rgbColor': {
                                'red': r,
                                'green': g,
                                'blue': b
                            }
                        }
                    }
                
            },
            'fields': 'bold,weightedFontFamily,fontSize,underline,foregroundColor'
        }
    },
    
 
    # Left align the content text
    
   
]
    

    # Execute the requests to insert and style the text
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    
    return(index+len(text))






def Mini_title(index, content_text,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
    
  

    #Insert_img(gmail_img,1)



    # Define the text to be inserted into the header and the document body
    
    

    # Define the requests to insert and style the header text
    requests = [
    # Insert normal content into the document body
    {
        'insertText': {
            'location': {
                'index': index,  # Insert right after the header
            },
            'text': content_text
        }
    },
    
    
    
    # Style the content text
    {
        'updateTextStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + len(content_text)  # Ensure this covers the content_text range
            },
            'textStyle': {
                'bold': False,
                'weightedFontFamily': {
                    'fontFamily': 'Lora'
                },
                'fontSize': {
                    'magnitude': 12,
                    'unit': 'PT'
                },
                'underline': False
            },
            'fields': 'bold,weightedFontFamily,fontSize,underline'
        }
    },
    
 
    # Left align the content text
    
   
]
    

    # Execute the requests to insert and style the text
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    insert_section_break( len(content_text),'CONTINUOUS',document_id)
    return(index + len(content_text)+1)
    
   
def Work_exp_data(start_index,text,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    request =[
        # Insert normal content into the document body
        {
            'insertText': {
                'location': {
                    'index': start_index,  # Insert at the specified index
                },
                'text': text
            }
        },
         {
            'insertText': {
                'location': {
                    'index': start_index + len(text),  # Insert at the specified index
                },
                'text': "add some accomplishments\n"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': start_index + len(text),  # Insert at the specified index
                },
                'text': "add some accomplishments\n"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': start_index + len(text),  # Insert at the specified index
                },
                'text': "add some accomplishments\n"
            }
        },
       
       
        # Style the content text
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': start_index ,
                    'endIndex': start_index + len(text) # Ensure this covers the text range
                },
                'textStyle': {
                    'bold': True,
                    'weightedFontFamily': {
                        'fontFamily': 'Spectral'
                    },
                    'fontSize': {
                        'magnitude': 15,
                        'unit': 'PT'
                    },
                    'underline': False
                },
                'fields': 'bold,weightedFontFamily,fontSize,underline'
            }
        },
        {
            'createParagraphBullets': {
                'range': {
                    'startIndex': start_index + len(text) ,  # Start index for bullets
                    'endIndex': start_index + len(text)+(len("add some accomplishments\n")+ (len("add some accomplishments\n")*2)) # Example end index (adjust as needed)
                },
                'bulletPreset': 'BULLET_DIAMONDX_ARROW3D_SQUARE'  # Specify the bullet style
            }
        },





    ]
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': request}).execute()
    
    return(  start_index + len(text)+(len("add some accomplishments\n")+ (len("add some accomplishments\n")*2)))

def Skill(start_index,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    request =[
        # Insert normal content into the document body
         {
            'insertText': {
                'location': {
                    'index': start_index,  # Insert at the specified index
                },
                'text': "add a skill\n"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': start_index ,  # Insert at the specified index
                },
                'text': "add a skill\n"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': start_index,  # Insert at the specified index
                },
                'text': "add a skill\n"
            }
        },
        
       
        # Style the content text
       
        {
            'createParagraphBullets': {
                'range': {
                    'startIndex': start_index+1 ,  # Start index for bullets
                    'endIndex': start_index +(len( "add a skill\n")+ (len( "add a skill\n")*2)) # Example end index (adjust as needed)
                },
                'bulletPreset': 'BULLET_DIAMONDX_ARROW3D_SQUARE'  # Specify the bullet style
            }
        },
        





    ]
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': request}).execute()
    return (start_index +(len( "add a skill\n")+ (len( "add a skill\n")*2)))







def Work_exp(start_index,text,document_id):
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    
    requests = [
        # Insert normal content into the document body
        {
            'insertText': {
                'location': {
                    'index': start_index,  # Insert at the specified index
                },
                'text': text
            }
        },
         
        # Style the content text
        {
            'updateTextStyle': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': start_index + len(text)  # Ensure this covers the text range
                },
                'textStyle': {
                    'bold': True,
                    'weightedFontFamily': {
                        'fontFamily': 'Spectral'
                    },
                    'fontSize': {
                        'magnitude': 20,
                        'unit': 'PT'
                    },
                    'underline': False
                },
                'fields': 'bold,weightedFontFamily,fontSize,underline'
            }
        },
         
        {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': start_index + len(text)
                },
                'paragraphStyle': {
                    'alignment': 'START',  # Add border
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {}}},
                        "width": {"magnitude": 1.5, "unit": "PT"},
                        "padding": {"magnitude": 0, "unit": "PT"},
                        "dashStyle": "SOLID"
                    },
                                    




                 
                    
                    
                    
                },
                'fields': 'alignment,borderBottom'
            }
        },
         
        
        

        
    ]

    
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    
    #add_bottom_border(service, start_index, start_index + len("WORK EXPERIENCE"))
    
    return (start_index + len(text)+1)










    



if __name__ == '__main__':
    document_id = "1AZyVSk_3INKs2LRXe0vV1GbHWOaVFl54vy1dLE4Avh0"
    creds = authenticate()
    service = build('docs', 'v1', credentials=creds)
    update_document_margins()
    Header("Enter name")
    lengthg =  Mini_title(1, 'hello123@gmail.com                                    (xxx)-xxx-xxxx                                                        New York, NY\n')
   
    w1=Work_exp(lengthg,"work exp")
    work_exp=Work_exp_data(w1,"job name\n")
    w2 = Work_exp_data(work_exp,"job name\n")

    project_exp= Work_exp(w2,"project exp\n")
    p1=Work_exp_data(project_exp-1,"project names\n")
    p2 = Work_exp_data(p1,"project names\n")


    education=Work_exp(p2,"EDUCATION\n")
    e1 = Education_data(15,0,0,0,education-1,"Cuny Hunter College - B.S., Computer Science\n",college_name="Cuny Hunter College ",degree= " - B.S., ", major= " Computer Science")
    e2 = Education_data_underneath(12,.60,.60,.60,e1,"agust 25 2023 - current                                                                                                                      New York, NY\n")


    
    skills = Work_exp(e2,"SKILL\n")
    end =Skill(skills-1)
    #send_to.share_document(document_id,'Suha221209885@gmail.com')

    

# Share the document and get the shareable link
    

    