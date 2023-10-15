from django.shortcuts import render
from django.http import HttpResponse , HttpRequest ,HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import os
import fnmatch
import markdown2 as md  # to handle markdown files
import random
from pathlib import Path


class UserInputForm(forms.Form):
    title = forms.CharField( widget=forms.TextInput(attrs={ 'placeholder':"Title.." , 'style' : 'width:300px;', 'class': 'form-control'}) )
    content = forms.CharField( widget=forms.Textarea(attrs={ 'placeholder':"Page Content..." , "rows":10, "cols" : 100, 'class': 'form-control'}) )

class SearchBoxForm(forms.Form):
    search = forms.CharField( widget=forms.TextInput(attrs={ 'placeholder':"Title.." }) )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_box_form" : SearchBoxForm()
    })


def newpage(request):
    if request.method == "POST":
        form = UserInputForm(request.POST)
        if form.is_valid() : 
            content = form.cleaned_data["content"]
            
            title = form.cleaned_data["title"]
            
            util.save_entry(title,content)
            
            return HttpResponseRedirect(reverse("entry" , kwargs = {"name" : title }))
        else :
            print("FORM isn't valid ")

    return render(request,"encyclopedia/newpage.html",{
        "form" : UserInputForm(),
        "search_box_form" : SearchBoxForm()
    }) 

'''
    This function will return a page that 'name' specified
    If there is no such a page (There is no related .md file) 
    it will generate a error page indicates there is no such a page and link to home page. 
'''
def find_file(directory, filename_pattern):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, filename_pattern):
                return os.path.join(root, file)
    return None  # Return None if the file is not found



def entry(request,name):
    # if there is no .md file in entries directory return error page

    markdown_file = find_file('entries/',f"{name}.md")
    if  markdown_file == None :
        return render(request,"encyclopedia/error.html",{
             "name" : name 
        })
    else :
        with open(markdown_file, 'r') as f:
            tempMd= f.read()
        tempHTML = md.markdown(tempMd)
        
        return render(request,"encyclopedia/entry.html",{
            "content" : tempHTML,
            "title" : name,
            "search_box_form" : SearchBoxForm()
        })


def random_page(request):
    size=0
    index = 0
    
    for root, dirs, files in os.walk('entries/'):
        for file in files:
            size+=1
    
    random_number = random.randint(1,size)
     
    for root, dirs, files in os.walk('entries/'):
        for file in files:
            index+=1
            if index == random_number : 
                random_file_name = Path(file).stem
                break

    dummy_request = HttpRequest()

    return HttpResponseRedirect(reverse("entry", kwargs={"name": random_file_name}))


def link_redirect(request,page_name) :
    return HttpResponseRedirect(reverse("entry" , kwargs = { "name" :page_name } )) 



def delete_file(file_path):
    print("Delete file entered")
    try:
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {str(e)}")


'''
This page will return a page that similar to newpage 
But it will contain its current content on the forms
---> Use similar aproach as newpage function
'''
import pdb

def edit_page(request,title):
    print(" Edit function called ")

    if request.method == "POST" :
        print("POST method invoked")
        form = UserInputForm(request.POST)
        if form.is_valid() :
            print("Form is valid")
            edited_title = form.cleaned_data["title"]
            edited_content = form.cleaned_data["content"]

            print(util.list_entries())
            print("/////////////////")
            util.delete_entry(title)
            print(util.list_entries())
            util.save_entry(edited_title,edited_content)
            return link_redirect(request,edited_title)
        else:
            print("Form isn't valid.")
        
    elif request.method == "GET":
        print("GET method invoked.")
        current_md_file = find_file('entries/',f"{title}.md")

        with open(current_md_file, 'r') as f:
            current_md_content= f.read()

        return render(request,"encyclopedia/edit_page.html",{
            "form" : UserInputForm(initial={ 'content' : current_md_content, 'title' : title }),
            "search_box_form" : SearchBoxForm(),
            "page_title" : title
        })



def search_result(request):

    # if keyword matched with one of the entry titles then redirect to this entry page
    # else list all of the titles that has keywords as a substring.
    user_input = SearchBoxForm(request.POST)

    if user_input.is_valid() : 
        keyword = user_input.cleaned_data["search"]
        list_of_entries = util.list_entries()
        try :
            index_of_keyword = list_of_entries.index(keyword)
            return HttpResponseRedirect(reverse("entry" , kwargs={"name" : list_of_entries[index_of_keyword]}))
        except :
            print(f" {keyword} wasn't found in entries ")
            search_results = []
            error_message = ""
            flag = False
            for page_title in list_of_entries : 
                if page_title.__contains__(keyword) :
                    search_results.append(page_title)
                    flag = True
            if flag == False : 
                error_message = "No entries matched with your search."
            return render( request , "encyclopedia/search_result.html",{
                "search_results" : search_results,
                "search_box_form" : SearchBoxForm(),
                "not_found_message" : error_message
            })
    else  : 
        print("User input wasn't valid.")