# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom as md
from xml.dom.minidom import parseString


#! --Elenco delle funzioni ricorsive: INIZIO

#funzione ric. per recuperare gli attributi
def child_attr(root, at =[]):
	
    if root.childNodes:
    	at = at
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                at.append((node.attributes.items()))
                child_attr(node)
    return at 

#funzione ric. per recuperare i nomi
def child_name(root, at =[]):
	
    if root.childNodes:
    	at = at
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                at.append((node.tagName))
                child_name(node)
    return at 

#funzione ric. per settare l'id ai nodi
def setId(root, n=0):
	
    if root.childNodes:
    	n = n
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                node.setAttribute("id", node.tagName+str(n))
                n = n+1
                setId(node)

#funzione ric. per recuperare l'id dei nodi
def getId(root, getid = []):
	
    if root.childNodes:	
    	getid=getid
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                getid.append(node.getAttribute('id'))
                getId(node)

    return getid


#funzione ric. per recuperare l'id dei nodi già presenti nel disegno
def getStoredId(root, getid = []):
	
    if root.childNodes:	
    	getid=getid
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.getAttribute('id') is not None:
                getid.append(node.getAttribute('id'))
                getStoredId(node)

    return getid

#!-- FINE FUNZIONI RICORSIVE

#!-- INIZIO MAIN
def main(file1):

	#implemento l'interfaccia DOM del file in input
	dom = md.parse(file1)
	root = dom.documentElement

	#popolo gli array con i dati delle funzioni ricorsive
	tagName= child_name(root)
	attri = child_attr(root)
	storedId = getStoredId(root)
	setId(root)
	get_Id = getId(root)
	
	#creo i nuovi array vuoti per mettere i dati "raffinati"
	newTag = []
	newAttr = []
	newId = []
	newStoredId = []
	

	#applico la raffinazione
	contatore = 0
	for i in attri:
		if(i !=[] and storedId !=""):
			newTag.append(tagName[contatore])
			newAttr.append(i)
			newId.append(get_Id[contatore])
			newStoredId.append(storedId[contatore])
		else:
			contatore = contatore
		contatore = contatore +1
	
	#apro il file in input
	file_input = open(file1, 'r')
	#preparo il file in output
	file_output = open('output.html', "w")

	#Intestazione HTML
	file_output.write("<!DOCTYPE html>")
	file_output.write("<html>")
	file_output.write("<body>")

	#copia del codice svg
	file_output.write(str(dom.toxml()))

	#applica una dimensione 400x400 all'elemento svg
	file_output.write("<script>document.getElementsByTagName('svg')[0].setAttribute('height', '400'); document.getElementsByTagName('svg')[0].setAttribute('width', '800'); </script>")
	
	#applico i vecchi id già presenti nel codice svg originale 
	genco = 0
	for enrico in newId:
		if(newStoredId[genco] != ""):
			file_output.write("<script>var svg"+str(genco)+" = document.getElementById('"+str(newId[genco])+"'); svg"+str(genco)+".setAttribute('id', '"+newStoredId [genco]+"' );</script>")
		genco = genco+1

	#inserisco i vecchi id in newId
	contatore2=0
	for j in newId:
		if(newStoredId[contatore2]!= ""):
			newId[contatore2] = newStoredId[contatore2]
		contatore2=contatore2+1
	
	#elementi della pagina HTML	
	file_output.write("<input type='button' onClick='history.go(0)' VALUE='Ripristina il disegno originale'>")
	file_output.write("<div id='desc'>")
	file_output.write("</div>")
	file_output.write("<div id='push' style='float: right; width: 540px; margin-right: 35px;'>")
	file_output.write("</div>")


	#parte dinamica di javascript
	cont = 0
	cont2 = 0
	cont3 = 0
	cont4 = 0	
	for tag in newTag:

		#elenco con i nomi degli elementi
		file_output.write("<script>var table = document.createElement('table');\nvar tr = document.createElement('tr');\n var th = document.createElement('th');\nvar node = document.createTextNode("+"'"+str(newId[cont])+"'"");\n th.appendChild(node);\ntr.appendChild(th);\ntable.appendChild(tr);\n var element = document.getElementById('desc');\n element.appendChild(table);\n var btnGet = document.createElement('BUTTON');\nvar btnSet = document.createElement('BUTTON');\nvar t = document.createTextNode('get');\n var s = document.createTextNode('set');\nbtnGet.appendChild(t);\n btnSet.appendChild(s);\n var att = document.createAttribute('onclick');\n att.value='getAttr"+str(newId[cont])+"()';\nbtnGet.setAttributeNode(att);\nelement.appendChild(btnGet);\nvar attSet = document.createAttribute('onclick');\n attSet.value='setAttr"+str(newId[cont])+"()';\nbtnSet.setAttributeNode(attSet);\nelement.appendChild(btnSet);\nvar push = document.getElementById('push'); </script>")

		#funzione get()
		file_output.write("<script>\nfunction getAttr"+str(newId[cont])+"(){\n\tdocument.getElementById('"+str(newId[cont])+"');\nif(push.childNodes[0] != null){\n\twhile(push.childNodes[0] != null){\n\tpush.removeChild(push.firstChild);\n}\n}\nelse if(push.childNodes[0] == null){")
		
		#estrazione dei valori e inserimento nei paragrafi creati dinamicamente
		for atb in newAttr[cont]:
			file_output.write("\n\tvar svg = document.getElementById('"+str(newId[cont])+"');\nvar svgAtt = svg.getAttribute("+"'"+newAttr[cont][cont2][0]+"'"");\nvar tag"+str(cont2)+"=document.createElement('p');\nvar testTag"+str(cont2)+" = document.createTextNode("+"'"+newAttr[cont][cont2][0]+" "+newId[cont]+"'"");\ntag"+str(cont2)+".appendChild(testTag"+str(cont2)+");\nvar attr"+str(cont2)+"=document.createElement('p');\nvar testAtt"+str(cont2)+" = document.createTextNode(svgAtt);\nattr"+str(cont2)+".appendChild(testAtt"+str(cont2)+");\npush.appendChild(tag"+str(cont2)+");\npush.appendChild(attr"+str(cont2)+");")
			cont2 = cont2+1
		file_output.write("}}</script>")
		cont2 = 0

		#funzione set()
		file_output.write("<script>\nfunction setAttr"+str(newId[cont])+"(){\n\tdocument.getElementById('"+str(newId[cont])+"');\nif(push.childNodes[0] != null){\n\twhile(push.childNodes[0] != null){\n\tpush.removeChild(push.firstChild);\n}\n}\nelse if(push.childNodes[0] == null){")
		
		#estrazione dei valori e inserimento nei paragrafi creati dinamicamente; creazione bottoni per chiamare la funzione setVal()
		for atb in newAttr[cont]:
			file_output.write("\n\tvar svg = document.getElementById('"+str(newId[cont])+"');\nvar svgAtt = svg.getAttribute("+"'"+newAttr[cont][cont2][0]+"'"");\nvar tag"+str(cont2)+"=document.createElement('p');\nvar testTag"+str(cont2)+" = document.createTextNode("+"'"+newAttr[cont][cont2][0]+" "+newId[cont]+"'"");\ntag"+str(cont2)+".appendChild(testTag"+str(cont2)+");\n var attr"+str(cont2)+"=document.createElement('input');\n attr"+str(cont2)+".setAttribute('id', "+"'"+newAttr[cont][cont2][0]+"'"");\n attr"+str(cont2)+".setAttribute('type','text');\n attr"+str(cont2)+".setAttribute('value',svgAtt);\n push.appendChild(tag"+str(cont2)+");\n push.appendChild(attr"+str(cont2)+");\n var btnApply = document.createElement('BUTTON');\n  var text = document.createTextNode('apply"+str(cont3)+"');\n btnApply.appendChild(text);\n var applyClick = document.createAttribute('onclick');\n applyClick.value='setVal"+str(cont3)+"()';\n btnApply.setAttributeNode(applyClick);\n push.appendChild(btnApply);")
			cont2 = cont2+1
			cont3= cont3+1
		file_output.write("}}</script>")
		cont2=0

		#funzione setVal()
		for atb in newAttr[cont]: 
			file_output.write("<script>function setVal"+str(cont4)+"(){\nvar input = document.getElementById("+"'"+newAttr[cont][cont2][0]+"'"").value; var svg = document.getElementById('"+str(newId[cont])+"');\n svg.setAttribute("+"'"+newAttr[cont][cont2][0]+"'"", input);}</script>")

			cont2 = cont2+1
			cont4= cont4+1
		cont = cont+1
		cont2=0

	#chiusura dei tag HTML
	file_output.write("</body>")
	file_output.write("</html>")
	
main(sys.argv[1])

#FINE
