import pandas as pd
import PySimpleGUI as sg
from pathlib import Path
import chardet
import matplotlib.pyplot as plt
import seaborn as sns

sg.theme("DarkBrown3")

layout = [[sg.B("Please select the CSV file",k="btn1"),sg.T(k="txt1")],[sg.ML(k="txt2",font=(None,14),size=(80,15))]]
win = sg.Window("Please select the file",layout)

def loadtext():
    global loadname, enc
    loadname = sg.popup_get_file("Please select the CSV file")
    if not loadname.lower().endswith('.csv'):
        return
    with open(loadname,"rb") as data:
        sns.set(font=["Meiryo","Yu Gothic","Hiragino Maru Gothic Pro"])
        data = pd.read_csv(loadname, usecols=["city","temperature", "latitude"])
        if len(data["city"]) == len(set(data["city"])):
            df = pd.DataFrame(data)
            df = df.dropna(axis=0)
            txt1 = "Data loaded"
            win["txt1"].update(txt1)
            df.plot.scatter(x="latitude",y="temperature",c="b",figsize=(30,8))
            plt.title("Regarding the correction between latitude and temperature")
            plt.show()
            print(df.shape)
        else:
           txt1 = "The data is duplicated.Please reload the file."
           win["txt1"].update(txt1)
            

while True:
    e,v = win.read()
    if e == "btn1":
        loadtext()
    if e == None:
        break
win.close()



layout = [[sg.T("Please enter the latitude")],[sg.T(k = "txt2")],[sg.I("",k="in1")],[sg.B( "execution" ,k = "btn"),sg.T(k = "txt1")]]
win = sg.Window("Average temperature estimation app",layout,font=(None,14),size=(500,150))

def execute():
 data = pd.read_csv(loadname,usecols=["city","temperature", "latitude"])
 if len(data["city"]) == len(set(data["city"])):
        data = pd.read_csv(loadname,index_col=0)
        df = pd.DataFrame(data)
        df = df.dropna(axis=0)
        df = df.drop(df[((df["latitude"]<=30) & (df["temperature"]<=20)) | (((df["latitude"]<=40) & (df["latitude"]>30)) & ((df["temperature"]<=10) | (df["temperature"]>=25))) | (((df["latitude"]<=50) & (df["latitude"]>40)) & ((df["temperature"]<=5) | (df["temperature"]>=20))) | ((df["latitude"]>50) & (df["temperature"]>=10))].index,axis=0)
        print(df.shape)
    
        x = df.drop("temperature",axis=1)
        t = df["temperature"]
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(x,t)
        from sklearn.model_selection import train_test_split
        x_train,x_test,t_train,t_test = train_test_split(x,t,test_size=0.4,random_state=1)
        model.fit(x_train,t_train)
    
        #print(model.score(x_train,t_train))
        #print(model.score(x_test,t_test))
        try:
            if float(v["in1"]) < 0 or float(v["in1"]) > 90:
                txt2 = f"The accuracy is,{round(model.score(x_test,t_test),2) * 100}％ "
                txt1 = f"Latitude ranges from 0° to 90°."
                win["txt2"].update(txt2)
                win["txt1"].update(txt1) 
            else:  
                y_pred = model.predict([[float(v["in1"])]])
                txt2 = f"The accuracy is,{round(model.score(x_test,t_test),2) * 100}％ "
                txt1 = f"The estimated average temperature is,{round(y_pred[0],2)}℃."
                win["txt2"].update(txt2)
                win["txt1"].update(txt1)     
        except ValueError:
            txt2 = f"The accuracy is,{round(model.score(x_test,t_test),2) * 100}％ "
            txt1 = "Please enter a number."
            win["txt2"].update(txt2)
            win["txt1"].update(txt1) 
 else:
    txt2 = "The model could not be trained correctly."
    win["txt2"].update(txt2)       

while True:
    e,v = win.read()
    if e == "btn":
        execute()
    if e == None:
        break
win.close()
