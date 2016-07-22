c = get_config()

# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook

# Notebook config
c.NotebookApp.certfile = u'/root/certs/mycert.pem' #location of your certificate file
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
c.NotebookApp.password = u'sha1:55f12841c5cf:41d09168bbde1dc5ea38fe4aba59cd0f82679c5a'  #the encrypted password we generated above
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = 8888
   