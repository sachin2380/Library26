from pickle import TRUE
from django.views.generic import View
from django.core.paginator import Paginator
import traceback
from .response import *

#Libsys import
from .constants import (LANGUAGE_SUCCESSFULLY_ADDED, LANGUAGE_DETAILS_FOUND, LANGUAGE_UPDATED_SUCCESSFULLY,
                        AUTHOR_SUCCESSFULLY_ADDED,AUTHOR_SUCCESSFULLY_FOUND, AUTHOR_DETAILS_UPDATED, AUTHOR_DETAILS_DELETED, AUTHOR_IMG_UPDATED,
                        BOOK_SUCCESSFULLY_ADDED,BOOK_DETAILS_FOUND, BOOK_DELETED, BOOK_INFO_FOUND, BOOK_ISSUED, BOOK_INFO_FOUND, BOOK_STATUS_CHANGE,
                        USER_ADDED, USER_DETAILS_FOUND, USER_DETAILS_UPDATED, USER_DELETED, USER_SUBSCRIPTION_ERR,
                        PUBLISHER_ADDED, PUBLISHER_DETAILS_FOUND, PUBLISHER_DETAILS_UPDATED, PUBLISHER_DELETED,
                        EBOOK_ADDED, EBOOK_DETAILS_FOUND, BOOK_LOCATION_UPDATED, EBOOK_DELETED,BOOK_DETAILS_NOT_FOUND,
                        FAVOURITE_BOOK_ADDED,
                        SUBSCRIPTION_ACTIVATED, SUBSCRIPTION_DEACTIVATED)

from .models import (Language, Author, Publisher, 
                    Book, HardBookInfo, Ebook, User ) 

from .exception import (FavouriteException, BookException, LanguageException,
                         AuthorException, PublisherException,
                        UserException, EbookException, HardBookInfoException, 
                        SubscriptionException, BookApprovalException )




class LanguageView(View):
    def __init__(self):
        self.response = init_response()

    def validate_language_name(self,language_name):
        language_list = Language.objects.all().values_list('name', flat=True)
        if language_name in language_list:
            raise LanguageException("Language already exist") 

    def validate_language_ids(self, language_ids):
        language_objs = Language.objects.filter(language_id__in=language_ids)
        if not language_objs:
            raise LanguageException("Language does not exist. please check the language id")
    def validate_language_param_keys(self,params):
        for key in ['name','script','about']:
            if not key in params.keys():
                raise LanguageException("All keys are required") 
    def validate_lang_value_params(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise LanguageException("keys has no value. please enter the value")            

    def post(self, request):
        params = request.POST.dict()
        try:
            self.validate_language_param_keys(params)
            self.validate_lang_value_params(params)
            language_name = params.get('name')
            self.validate_language_name(language_name)
            Language.objects.add_language_details(params)
            self.response['res_str'] = LANGUAGE_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)


    def validate_language_params(self,params):
        for key in ['language_id']:
            if not key in params.keys():
                raise LanguageException("language ids are required")                 
        
    def get(self,request):
        params = request.GET.dict()
        try:
            self.validate_language_params(params)
            self.validate_lang_value_params(params)
            language_ids = params.get('language_id').strip().split(',')
            self.validate_language_ids(language_ids)
            language_details = Language.objects.get_langauge_details(language_ids)
            self.response['res_data'] = language_details
            self.response['res_str'] = LANGUAGE_DETAILS_FOUND
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_language_params_keys(self,params):
        for key in ['language_id','about','name','script']:
            if not key in params.keys():
                raise LanguageException("All keys are required")                  

    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_language_params_keys(params)
            self.validate_lang_value_params(params)
            language_id = params.get('language_id').strip().split(',')
            self.validate_language_ids(language_id)
            language_details = Language.objects.update_langauge_details(params)
            self.response['res_data'] = language_details
            self.response['res_str'] = LANGUAGE_UPDATED_SUCCESSFULLY 
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)        
        except Exception as ex:
            self.response['res_str'] =  traceback.format_exc()
            return send_400(self.response)          

class AuthorView(View):
    def __init__(self):
        self.response = init_response()

    def validate_author_ids(self,author_ids):
        author_objs = Author.objects.filter(author_id__in=author_ids)
        if not author_objs:
            raise AuthorException("Author does not exist please check Author id")

    def validate_author_param(self,params):
        for key in ['email_id','name']:
            if not key in params.keys():
                raise AuthorException("All keys are required")

    def validate_author_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise AuthorException("keys has no value. please enter the value")              

    def post(self, request):
        params = request.POST.dict()
        try:
            self.validate_author_param(params)
            self.validate_author_params_value(params)
            author_image = request.FILES['picture']
            Author.objects.add_author(params,author_image)
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_author_params_key(self,params):
        for key in ['author_id']:
            if not key in params.keys():
                raise AuthorException("All keys are required")
      
    def get(self,request):
        params = request.GET.dict()
        try:
            self.validate_author_params_key(params)
            self.validate_author_params_value(params)
            author_ids = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_ids)
            author_detail = Author.objects.get_author_details(author_ids)
            self.response['res_data'] = author_detail
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_FOUND
            return send_200(self.response)
        except AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_author_params(self,params):
        for key in ['author_id','email_id','name']:
            if not key in params.keys():
                raise AuthorException("All keys are required") 
  
    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_author_params(params)
            self.validate_author_params_value(params)
            author_id = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_id)
            author_detail = Author.objects.update_author_details(params)
            self.response['res_data'] = author_detail
            self.response['res_str'] = AUTHOR_DETAILS_UPDATED
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] =traceback.format_exc()
            return send_400(self.response)          
  
    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_author_params_key(params)
            self.validate_author_params_value(params)
            author_ids = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_ids)
            Author.objects.filter(author_id__in=author_ids).delete()
            self.response['res_str'] = AUTHOR_DETAILS_DELETED   
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)             
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)  

class BookView(View):
    def __init__(self):
        self.response = init_response()


    def validate_book_ids(self,book_id):
        book_objs = Book.objects.filter(book_id__in=book_id)
        if not book_objs:
            raise BookException("Invalid Book id") 

    def validate_language_id_author_id_publisher_id(self,language_id,publisher_id,author_id):
        language_obj = Language.objects.get(language_id = language_id)
        publisher_obj = Publisher.objects.get(publisher_id = publisher_id)
        author_obj = Author.objects.get(author_id=author_id)
        if not (language_obj and publisher_obj and author_obj):
            raise BookException("Invalid language id or author id or publisher id. enter language id or author id or publisher id ")
        return publisher_obj,language_obj,author_obj


    def validate_book_param(self,params):
        for key in ['name','language_id','publisher_id','author_id','book_type','category','extra_det']:
            if not key in params.keys():
                raise BookException("All keys are required") 

    def validate_book_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise BookException("keys has no value. please enter the value")               
                                           

    def post(self,request,*args, **kwargs):

        def __init__(self):
            self.response = init_response()

        params = request.POST.dict()    
        try:   
            self.validate_book_param(params) 
            self.validate_book_params_value(params)                
            language_id = params.get('language_id')
            publisher_id = params.get('publisher_id')
            author_id = params.get('author_id')
            publisher_obj,language_obj,author_obj = self.validate_language_id_author_id_publisher_id(language_id,publisher_id,author_id)
            Book.objects.add_book_details(params,publisher_obj,language_obj,author_obj)
            self.response['res_str'] = BOOK_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

    def validate_book_params(self,params):
        for key in ['book_id','per_page','page']:
            if not key in params.keys():
                raise BookException("All keys are required")  

    def get(self, request):
        params=request.GET.dict()
        try:
            self.validate_book_params(params)
            self.validate_book_params_value(params)
            per_page= params.get('per_page')
            book_ids = params.get('book_id').strip().split(',')
            self.validate_book_ids(book_ids)
            book = Book.objects.get_book_details(book_ids)
            paginator = Paginator(book,per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.page(page_number)
            book_data = page_obj.object_list
            self.response['res_data'] = book_data
            self.response['res_str'] = BOOK_DETAILS_FOUND
            return send_200(self.response)
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_book_params_key(self,params):
        for key in ['book_id']:
            if not key in params.keys():
                raise BookException("All keys are required")             
   
    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_book_params_key(params)
            self.validate_book_params_value(params)
            book_id = params.get('book_id').strip().split(',')
            self.validate_book_ids(book_id)
            Book.objects.filter(book_id__in=book_id).delete()
            self.response['res_str'] = BOOK_DELETED 
            return send_200(self.response)       
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)  
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class UserView(View):
    def __init__(self):
        self.response = init_response()


    def validate_user_ids(self,user_id):
        user_objs = User.objects.filter(user_id__in = user_id)
        if not user_objs:
            raise UserException("User does not exist. check User Id")
        # return user_objs
    def validate_existing_user(self,aadhar_id):
        user_obj = User.objects.filter(aadhar_id=aadhar_id)
        if user_obj:
            raise UserException("User already exist") 
            
    def validate_user_param(self,params):
        for key in ['first_name', 'last_name', 'mobile_no', 'email_id', 'aadhar_id', 'role']:
            if not key in params.keys():
                raise UserException("All keys are required")

    def validate_user_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise UserException("keys has no value. please enter the value")                                 
   
    def post(self, request):
        params = request.POST.dict()
        try:
            self.validate_user_param(params)
            self.validate_user_params_value(params)
            aadhar_id = params.get("aadhar_id")
            self.validate_existing_user(aadhar_id)
            User.objects.add_user(params)
            self.response['res_str'] = USER_ADDED
            return send_201(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)  


    def validate_user_params_key(self,params):
        for key in ['user_id']:
            if not key in params.keys():
                raise UserException("user_id key is required")               

    def get(self,request):
        params = request.GET.dict()
        try:
            self.validate_user_params_key(params)
            self.validate_user_params_value(params)
            user_ids = params.get('user_id').strip().split(',')
            self.validate_user_ids(user_ids)
            user = User.objects.get_user_details(user_ids)
            self.response['res_data'] = user
            self.response['res_str'] = USER_DETAILS_FOUND
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)   

    def validate_user_params(self,params):
        for key in ['user_id','mobile_no', 'email_id', 'role']:
            if not key in params.keys():
                raise UserException("All keys are required")               

    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_user_params(params)
            self.validate_user_params_value(params)
            user_id = params.get('user_id')
            self.validate_user_ids(user_id)
            user =  User.objects.update_user_details(params)
            self.response['res_str'] = USER_DETAILS_UPDATED
            self.response['res_data'] = user
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response) 
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)       

    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_user_params_key(params)
            self.validate_user_params_value(params)
            user_id = params.get('user_id').strip().split(',')
            self.validate_user_ids(user_id)
            User.objects.filter(user_id__in=user_id).delete()
            self.response['res_str'] = USER_DELETED
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)       
   
class PublisherView(View):
    def __init__(self):
        self.response = init_response()

    def validate_publisher_ids(self,publisher_ids):
        publisher_objs = Publisher.objects.filter(publisher_id__in = publisher_ids)
        if not publisher_objs:
            raise PublisherException("Publisher does not exist please check publisher id") 

    def validate_publisher_params(self,params):
        for key in ['name', 'contact_details']:
            if not key in params.keys():
                raise PublisherException("All keys are required")

    def validate_publisher_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise PublisherException("keys has no value. please enter the value")                                 
               

    def post(self, request):
        params = request.POST.dict()
        try:
            self.validate_publisher_params(params)
            self.validate_publisher_params_value(params)
            Publisher.objects.add_publisher_details(params)
            self.response['res_str'] = PUBLISHER_ADDED
            return send_201(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex: 
            self.response['res_str'] = traceback.format_exc() 
            return send_400(self.response)            

    def validate_publisher_params_key(self,params):
        for key in ['publisher_id']:
            if not key in params.keys():
                raise PublisherException("publisher id key is required")

    def get(self, request):
        params = request.GET.dict()
        try:
            self.validate_publisher_params_key(params)
            self.validate_publisher_params_value(params)
            publisher_ids = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_ids)
            publisher_det = Publisher.objects.get_publisher_details(publisher_ids)
            self.response['res_data'] = publisher_det
            self.response['res_str'] = PUBLISHER_DETAILS_FOUND
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)          

    def validate_publisher_param(self,params):
        for key in ['publisher_id','name','contact_details']:
            if not key in params.keys():
                raise PublisherException("all keys are  required")        

    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_publisher_param(params)
            self.validate_publisher_params_value(params)
            publisher_id = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_id)
            publisher_details = Publisher.objects.update_publisher_details(params)
            self.response['res_data'] = publisher_details
            self.response['res_str'] = PUBLISHER_DETAILS_UPDATED
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 
    
    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_publisher_params_key(params)
            self.validate_publisher_params_value(params)
            publisher_id = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_id)
            Publisher.objects.filter(publisher_id__in=publisher_id).delete()
            self.response['res_str'] = PUBLISHER_DELETED
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class EbookView(View):

    def __init__(self):
        self.response = init_response()

    def validate_ebook_ids(self,book_id):
        ebook_objs = Ebook.objects.filter(book_id__in = book_id)
        if not ebook_objs:
            raise EbookException("Ebook Id does not exist")        
    def check_ebook_existing(self,book_id):
        ebook_obj = Ebook.objects.select_related("ebook").all().values_list("ebook", flat=True)[::1]
        if int(book_id) in ebook_obj:
            raise EbookException("Ebook already exist")
    def validate_book_id_user_id(self,book_id):
        book_obj = Book.objects.filter(book_id=book_id)
        user_obj = Book.objects.filter(book_id=book_id)
        if not (user_obj and book_obj):
            raise EbookException("Book id or user id does not exist. Please enter valid book id or user id")

    def validate_book_type(self,book_id):
        book_obj = Book.objects.get(book_id=book_id)
        book_type = book_obj.book_type
        if not (book_type=="ebook"):
            raise EbookException("This action is not allowed because this is not soft copy of the book. please enter valid book id")


    def validate_ebook_params(self,params):
        for key in ['book_id','user_id','location']:
            if not key in params.keys():
                raise EbookException("all keys are required")

    def validate_ebook_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise EbookException("keys has no value. please enter the value")              

    def post(self,request):
        params = request.POST.dict()
        try:
            self.validate_ebook_params(params)
            self.validate_ebook_params_value(params)
            book_id = params.get('book_id')
            user_id = params.get('user_id')
            location = params.get('location')
            self.validate_book_id_user_id(book_id)
            self.check_ebook_existing(book_id)
            self.validate_book_type(book_id)
            book_obj = Book.objects.get(book_id = book_id)
            user_obj = User.objects.get(user_id=user_id)
            location = params.get("location")
            Ebook.objects.add_ebook(book_obj, location, user_obj)
            self.response['res_str'] = EBOOK_ADDED
            return send_201(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)   
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

    def validate_ebook_params_key(self,params):
        for key in ['ebook_id']:
            if not key in params.keys():
                raise EbookException("book_id key is required")            

    def get(self,request):
        params =  request.GET.dict()
        try:
            self.validate_ebook_params_key(params)
            self.validate_ebook_params_value(params)
            book_id = params.get('ebook_id').strip().split(',')
            self.validate_ebook_ids(book_id)
            ebook = Ebook.objects.get_ebook_info(book_id)
            self.response['res_data'] = ebook
            self.response['res_str'] = EBOOK_DETAILS_FOUND
            return send_200(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def validate_ebook_param(self,params):
        for key in ['ebook_id','location']:
            if not key in params.keys():
                raise EbookException("all keys are required")             

    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_ebook_param(params)
            self.validate_ebook_params_value(params)
            ebook_id = params.get("ebook_id").strip().split(',')
            location = params.get('location')
            self.validate_ebook_ids(ebook_id)
            book_obj = Ebook.objects.get(book_id__in=ebook_id)
            book_obj.book_location = location   
            book_obj.save(update_fields=['book_location'])  
            self.response['res_str'] = BOOK_LOCATION_UPDATED
            return send_200(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_ebook_params_key(params)
            self.validate_ebook_params_value(params)
            book_id = params.get("ebook_id").strip().split(',')
            self.validate_ebook_ids(book_id)
            Ebook.objects.filter(book_id__in=book_id).delete()
            self.response['res_str'] = EBOOK_DELETED
            return send_200(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class HardBookInfoView(View):
    def __init__(self):
        self.response = init_response()

    def validate_hardcopy_ids(self,hardCopy_id):
        bookinfo_objs = HardBookInfo.objects.filter(hardCopy_id__in = hardCopy_id)
        if not bookinfo_objs:
            raise HardBookInfoException("Invalid hardCopy Id") 

    def valiate_book_count(self,user_id):
        hardcopybook_list = list(HardBookInfo.objects.select_related("lentTo").all().values_list("lentTo", flat=True))
        book_count = hardcopybook_list.count(int(user_id))
        if book_count >5:
            raise HardBookInfoException("More than 5 books not allowed")


    def check_nbook_existing(self,user_id,book_id):
        user_list = list(HardBookInfo.objects.select_related("lentTo").all().values_list("lentTo", flat=True))
        book_lis = list(HardBookInfo.objects.select_related("book_name").all().values_list("book_name", flat=True))
        if ((int(user_id) in user_list) and (int(book_id) in book_lis)):
            raise HardBookInfoException("Book already assign to user")            

    def validate_book_id(self,book_id):
        book_obj = Book.objects.filter(book_id=book_id)
        if not book_obj:
            raise HardBookInfoException("Book id does not exist. please enter valid book id")

    def validate_book_type(self,book_id):
        book_obj = Book.objects.get(book_id=book_id)
        book_type = book_obj.book_type
        if not (book_type=="nbook" and book_obj):
            raise HardBookInfoException("this is not hardcopy of the book. please enter valid book id")

    def validate_hardbook_params(self,params):
        for key in ['book_id', 'user_id','isLent']:
            if not key in params.keys():
                raise HardBookInfoException("All keys are mandatory")

    def validate_hardcopy_book_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise HardBookInfoException("keys has no value. please enter the value")              
            

    def post(self,request):
        params = request.POST.dict()
        try:
            self.validate_hardbook_params(params)
            self.validate_hardcopy_book_params_value(params)
            user_id = params.get('user_id')
            book_id = params.get('book_id')
            self.validate_book_id(book_id)
            self.validate_book_type(book_id)
            self.check_nbook_existing(user_id,book_id)
            book_obj = Book.objects.get(book_id=book_id)
            isLent = params.get('isLent')
            self.valiate_book_count(user_id)
            user_obj = User.objects.get(user_id=user_id)
            if user_obj.subscription == True:
                HardBookInfo.objects.issue_book(book_obj,isLent,user_obj)
                self.response['res_str'] = BOOK_ISSUED
            else:
                self.response['res_str'] = USER_SUBSCRIPTION_ERR   
            return send_201(self.response)
        except HardBookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)   
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 


    def validate_hardbook_params_key(self,params):
        for key in ['hardCopy_id']:
            if not key in params.keys():
                raise HardBookInfoException("hardCopy_id key is  required")                

    def get(self,request):
        params = request.GET.dict()
        try:
            self.validate_hardbook_params_key(params)
            self.validate_hardcopy_book_params_value(params)
            hardCopy_id = params.get('hardCopy_id').strip().split(',')
            self.validate_hardcopy_ids(hardCopy_id)
            book_info =  HardBookInfo.objects.get_issue_book_info(hardCopy_id)
            self.response['res_data'] = book_info
            self.response['res_str'] = BOOK_INFO_FOUND
            return send_200(self.response)
        except HardBookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)
        

    def delete(self,request):
        params = request.GET.dict()
        try:
            self.validate_hardbook_params_key(params)
            self.validate_hardcopy_book_params_value(params)
            hardCopy_id = params.get('hardCopy_id').strip().split(',')
            self.validate_hardcopy_ids(hardCopy_id)
            HardBookInfo.objects.filter(hardCopy_id__in=hardCopy_id).delete()
            self.response['res_str'] = BOOK_DELETED
            return send_200(self.response)
        except HardBookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)    

class BookApproval(View):
    def __init__(self):
        self.response = init_response()

    def validate_user_role(self,user_id):
        user_obj = User.objects.get(user_id=user_id)
        user_role = user_obj.role
        if not (user_role=="moderator"):
            raise BookApprovalException("User has no permission to perform this action.only moderator have permission to change the book status")
    def validate_book_id(self,book_id):
        book_objs = Ebook.objects.filter(book_id=book_id)
        if not book_objs:
            raise BookApprovalException("Book does not exist. enter valid book id")

    def validate_book_approval_params(self,params):
        for key in ['book_id', 'user_id','approval_status']:
            if not key in params.keys():
                raise BookApprovalException("All keys are required")

    def validate_book_approval_params_value(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise BookApprovalException("keys has no value. please enter the value")              

    def post(self,request):
        params = request.POST.dict()
        try:
            self.validate_book_approval_params(params)
            self.validate_book_approval_params_value(params)
            book_id = params.get('book_id')
            user_id = params.get('user_id')
            approval_status = params.get('approval_status')
            self.validate_user_role(user_id)
            self.validate_book_id(book_id)
            book_obj = Ebook.objects.get(book_id=book_id)
            book_obj.approval_status =  approval_status 
            book_obj.save(update_fields = ['approval_status'])
            self.response['res_str'] = BOOK_STATUS_CHANGE
            return send_201(self.response)    
        except BookApprovalException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)

class SearchView(View):

    def __init__(self):
        self.response = init_response()

    def validate_search_params(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise BookApprovalException("keys has no value. please enter the value")

    def validate_empty_dict(self,params):
        if len(params)==0:
            raise BookApprovalException("'book_name' or 'author_name' or 'publisher_name' or 'category' keys is required")

    def get(self, request):
        params = request.GET.dict()
        try:
            self.validate_empty_dict(params)
            self.validate_search_params(params)
            author = params.get('author_name')
            book_name = params.get('book_name')
            category = params.get('category')
            publisher = params.get('publisher_name')
            if author:
               book_list=  list(Book.objects.filter(author__name__icontains=author).values_list("name",flat=True))
            elif book_name:
                book_list = list(Book.objects.filter(name__icontains=book_name).values_list("name",flat=True))
            elif publisher:
                book_list = list(Book.objects.filter(publisher__name__contains=publisher).values_list("name",flat=True))
            elif category:
                book_list = list(Book.objects.filter(category__icontains=category).values_list("name",flat=True))
            if not len(book_list)==0:
                self.response['res_data'] = book_list
                self.response['res_str'] = BOOK_DETAILS_FOUND     
            else:
                self.response['res_str'] = BOOK_DETAILS_NOT_FOUND 
            return send_200(self.response)  
        except BookApprovalException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
        except Exception as ex:
            self.response['res_data'] = traceback.format_exc()
            self.response['res_str'] = str(ex)
            return send_400(self.response)     

class FavouriteBookView(View):
    
    def __init__(self):
        self.response = init_response()

    def validate_user_book_ids(self,book_id, user_id):
        user_obj = User.objects.filter(user_id=user_id)
        book_objs = Book.objects.filter(book_id__in=book_id)
        if not (book_objs and user_obj):
            raise FavouriteException("user id or book id error. check the user id and book id ") 

    def validate_favourite_params(self,params):
        for key in ['user_id', 'book_id']:
            if not key in params.keys():
                raise FavouriteException("All keys are mandatory")

    def validate_fav_key_params(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise FavouriteException("keys has no value. please enter the value")
            

    def post(self,request):
        params = request.POST.dict()
        try:
            self.validate_favourite_params(params)
            self.validate_fav_key_params(params)
            book_id = params.get('book_id').strip().split(',')
            user_id = params.get('user_id')
            self.validate_user_book_ids(book_id,user_id)
            User.objects.add_favourite_book(book_id,user_id)
            self.response['res_str'] = FAVOURITE_BOOK_ADDED
            return send_201(self.response)
        except FavouriteException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response)
                   

class Subscription(View):

    def __init__(self):
        self.response = init_response()

    def validate_user(self,user_id):
        user_obj = User.objects.filter(user_id=user_id)
        if not user_obj:
            raise SubscriptionException("User does not exist. enter valid user id")

    def validate_subscription_choice(self,choice):
        if not (int(choice)==1 or int(choice)==0):
            raise SubscriptionException("Enter valid choice either 0 or 1. you have enter other than 0 or 1")

    def validate_subscription_params(self,params):
        for key in ['user_id', 'choice']:
            if key not in params.keys():
                raise SubscriptionException("All keys are mandatory")

    def validate_subscription_key_params(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise SubscriptionException("keys has no value. please enter the value")

    def put(self,request):
        params = request.GET.dict()
        try:
            self.validate_subscription_params(params)
            self.validate_subscription_key_params(params)
            user_id= params.get('user_id')
            choice = params.get('choice')
            self.validate_user(user_id)
            self.validate_subscription_choice(choice)
            user_det = User.objects.update_subscription(user_id, choice)
            if int(choice)==1:
                self.response['res_str'] = SUBSCRIPTION_ACTIVATED
            else:
                self.response['res_str'] = SUBSCRIPTION_DEACTIVATED  
            self.response['res_data'] = user_det
            return send_200(self.response)
        except SubscriptionException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 


class UpdateAuthorImg(View):
    
    def __init__(self):
        self.response = init_response()

    def validate_author_id_key(self,params):
        for key in ['author_id']:
            if not key in params.keys():
                raise AuthorException("author_id key is required")

    def validate_author_key_params(self,params):
        for key, value in params.items():
            if len(value)==0:
                raise AuthorException("keys has no value. please enter the value")            
                
    def validate_author_id(self,author_id):
        author_objs = Author.objects.filter(author_id=author_id)
        if not author_objs:
            raise AuthorException("Author id does not exist.please enter valid author id")


    def post(self,request):
        params = request.POST.dict()
        try:
            self.validate_author_id_key(params)
            self.validate_author_key_params(params)
            picture = request.FILES['picture']
            author_id = params.get('author_id')
            self.validate_author_id(author_id)
            author_obj = Author.objects.get(author_id=author_id)
            author_obj.picture = picture
            author_obj.save(update_fields=['picture'])
            self.response['res_str'] = AUTHOR_IMG_UPDATED
            return send_201(self.response)
        except AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            self.response['res_str'] = traceback.format_exc()
            return send_400(self.response) 

        
