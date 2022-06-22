

module wt
using  HTTP
using JSON 
using DotEnv

function __init__()
    print("module hass been loaded")
    print('\n', "this is your first time useing the module, so you will have to write a file with you user name and password, give make_file(username,passowrd)")


end

function combine(user,password)
    a="client_id=support_token_server&client_secret=4support_server2work&grant_type=password&username="*user
    b="&password="*password
    return a*b
end 

function make_file(user,password)
    header = Dict("Content-Type" => "application/x-www-form-urlencoded")
    b = combine(user,password) 
    resp=HTTP.post("https://support.econjobmarket.org/oauth2/token",headers=header,body=b)

    t=String(resp.body)
    ref_token=JSON.parse(t)["refresh_token"]
    b = Dict(
    "client_id"=> "support_token_server",
    "client_secret"=> "4support_server2work",
    "grant_type"=> "refresh_token",
    "refresh_token"=>ref_token)
    bb=HTTP.Form(b)
    response =HTTP.post("https://support.econjobmarket.org/oauth2/token", body=bb)  
    t=String(response.body)
    access_token=JSON.parse(t)["access_token"]
    #dict1= Dict("User"=>user,"Password"=>password,"REF_TOKEN"=>ref_token,"ACCESS_TOKEN"=>access_token)
    #stringdata = JSON.json(dict1)
    open("user.env", "w") do f
        write(f,"user="*user*"\n")
        write(f,"password="*password*"\n")
        write(f,"ref_token="*ref_token*"\n")
        write(f,"access_token="*access_token*"\n")
    end  

        return  [user,password,ref_token,access_token]
end


function  file_y_n(link)
    try
        
        DotEnv.config("user.env")

        list= [link,ENV["user"],ENV["password"],ENV["ref_token"],ENV["access_token"]]
        print(list)
        return list
    catch 
        print("Create a file with your username and passowrd, useing makefile()")
    end 
    

    
end
    
    
function get_data(list)
    link=list[1]
    access_token=list[5]

    headers = Dict(
    "Accept"=> "application/json",
    "Authorization"=> "Bearer "* access_token)

    response = HTTP.get(link, headers=headers) 
    t=String(response.body)
    slice=JSON.parse(t)

    
    try
        d=slice[1]
        return slice
    catch
        return 0

    end 
end 

function  get_token(list)
    user=list[2]
    password=list[3]
    
    try
        l=make_file(user,password)
        return [list[1],l[1],l[2],l[3],l[4]]

       
    catch 
        return 2
    end 
end 
        



       
function run(list)
    slice=get_data(list)
    if (slice==0)
        list=get_token(list)
        print(list)
        slice=get_data(list)
    end 

    return slice
end 


'''
#method one, create and use a file (best way)
'''



function full_run(link)
    t=file_y_n(link)
    slice=run(t)
    return slice
end 


end 

#wt.make_file("useer","passowrd")
#l=wt.file_y_n("https://support.econjobmarket.org/api/slice")
#wt.run(l)
wt.full_run("https://support.econjobmarket.org/api/slice")