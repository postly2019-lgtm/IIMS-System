2026-01-01T22:33:42.203858180Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:42.203864578Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:42.203871773Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:42.203877804Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:42.203883778Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:42.203891550Z [err]                                                  ^
2026-01-01T22:33:42.203898684Z [err]  ^^^^
2026-01-01T22:33:42.212134720Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:43.818932941Z [err]  Traceback (most recent call last):
2026-01-01T22:33:43.818940017Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:43.818994697Z [err]      main()
2026-01-01T22:33:43.819004094Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:43.819011736Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:43.819019397Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:43.819026522Z [err]      utility.execute()
2026-01-01T22:33:43.819032508Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:43.819038021Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:43.819126140Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:43.819141017Z [err]      self._setup(name)
2026-01-01T22:33:43.819149145Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:43.819156245Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:43.819163779Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:43.819171279Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:43.819180086Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:44.908237935Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:44.908246159Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:44.908255489Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:44.908262828Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:44.908269121Z [err]  ^^
2026-01-01T22:33:44.908276209Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:44.908283323Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:44.908531131Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:44.908548188Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:44.908562755Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:44.908570292Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:44.908577016Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:44.908583392Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:45.948135689Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:45.948528201Z [err]                                                  ^^^^^
2026-01-01T22:33:45.948534179Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:45.948540287Z [err]  Traceback (most recent call last):
2026-01-01T22:33:45.948546292Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:45.948553074Z [err]      main()
2026-01-01T22:33:45.948560217Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:45.948566977Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:45.948573337Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:45.948582423Z [err]      utility.execute()
2026-01-01T22:33:45.954284029Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:45.954298715Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:45.954307161Z [err]      self._setup(name)
2026-01-01T22:33:45.954447533Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:45.954455332Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:45.954464571Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:45.954471082Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:45.954478257Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:45.954483742Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:45.954490096Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:46.918509066Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:46.918515375Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:46.918524671Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:46.918530914Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:46.918537226Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:46.918544588Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:46.918550760Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:46.918557044Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:46.918564115Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:46.918571522Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:46.918577824Z [err]                                                  ^^^^^
2026-01-01T22:33:46.918584423Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:48.127500118Z [err]  Traceback (most recent call last):
2026-01-01T22:33:48.127506705Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:48.127513125Z [err]      main()
2026-01-01T22:33:48.127518902Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:48.127524867Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:48.127530443Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:48.127536043Z [err]      utility.execute()
2026-01-01T22:33:48.127541852Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:48.127547491Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:48.127553031Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:48.127563095Z [err]      self._setup(name)
2026-01-01T22:33:48.127568688Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:48.127574948Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:48.127581589Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:48.127587950Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:48.130245861Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:48.130289425Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:48.130299542Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:49.197633582Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:49.197639669Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:49.197646669Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:49.197652170Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:49.197657838Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:49.197663663Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:49.197669739Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:49.197675096Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:49.197680979Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:49.197687653Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:49.197694320Z [err]                                                  ^^^^^
2026-01-01T22:33:49.197699834Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:50.266344003Z [err]  Traceback (most recent call last):
2026-01-01T22:33:50.266350666Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:50.266357234Z [err]      main()
2026-01-01T22:33:50.266363999Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:50.266371597Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:50.266378482Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:50.266385405Z [err]      utility.execute()
2026-01-01T22:33:50.266392003Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:50.266400141Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:50.266407237Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:50.266413696Z [err]      self._setup(name)
2026-01-01T22:33:50.266420493Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:50.266427065Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:50.266433772Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:50.266440799Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:50.266447620Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:50.266454650Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:50.266461975Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:50.266468925Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:50.266475533Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:51.338461268Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:51.338467760Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:51.338474602Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:51.338484293Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:51.338490371Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:51.338496548Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:51.338503987Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:51.338514979Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:51.338521697Z [err]                                                  ^^^^^
2026-01-01T22:33:51.338527768Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:51.338539552Z [err]  Traceback (most recent call last):
2026-01-01T22:33:51.338546171Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:51.338552400Z [err]      main()
2026-01-01T22:33:51.347010016Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:51.347023002Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:51.347030057Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:51.347036631Z [err]      utility.execute()
2026-01-01T22:33:51.347042761Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:52.038508025Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:52.038520176Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:52.038528216Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:52.038543528Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:52.038571210Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:52.038571254Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:52.038581155Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:52.038581944Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:52.038591598Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:52.038591756Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:52.038594253Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:52.038611607Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:52.038613728Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:52.038622073Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:52.038623198Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:52.038631769Z [err]      self._setup(name)
2026-01-01T22:33:52.038639276Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:52.046355926Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:52.046362125Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:52.046369540Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:52.046377883Z [err]                                                  ^^^^^
2026-01-01T22:33:52.046384761Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:54.255603583Z [err]                                                  ^^^^^
2026-01-01T22:33:54.255612826Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:54.255639910Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:54.255647604Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:54.255655071Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:54.255659587Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:54.255667932Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:54.255670023Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:54.255677590Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:54.255679939Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:54.255689888Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:54.255851481Z [err]  Traceback (most recent call last):
2026-01-01T22:33:54.255857556Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:54.255863340Z [err]      main()
2026-01-01T22:33:54.255870333Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:54.255876265Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:54.255883478Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:54.255894203Z [err]      utility.execute()
2026-01-01T22:33:54.255900163Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:54.255910656Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:54.255916927Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:54.255922851Z [err]      self._setup(name)
2026-01-01T22:33:54.255928830Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:54.255935769Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:54.255941972Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:54.255948671Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:54.255956071Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:54.255961773Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:54.255968321Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:54.255974760Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:56.368767899Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:56.369141041Z [err]      main()
2026-01-01T22:33:56.369154236Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:56.369164053Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:56.369171955Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:56.369179556Z [err]      utility.execute()
2026-01-01T22:33:56.369187234Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:56.369194998Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:56.369201260Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:56.369208236Z [err]      self._setup(name)
2026-01-01T22:33:56.369215849Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:56.369222207Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:56.369229029Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:56.369235174Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:56.369241398Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:56.369247868Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:56.369254011Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:56.369261570Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:56.369271789Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:56.369278802Z [err]  Traceback (most recent call last):
2026-01-01T22:33:57.215334348Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:57.215340074Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:57.215345679Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:57.215350643Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:57.215356047Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:57.215361436Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:57.215367528Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:57.215373108Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:33:57.215378498Z [err]                                                  ^^^^^
2026-01-01T22:33:57.215385809Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:33:58.491890247Z [err]  Traceback (most recent call last):
2026-01-01T22:33:58.491897346Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:33:58.491903650Z [err]      main()
2026-01-01T22:33:58.491910432Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:33:58.491917643Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:33:58.491923779Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:33:58.491929872Z [err]      utility.execute()
2026-01-01T22:33:58.491937653Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:33:58.491943841Z [err]      settings.INSTALLED_APPS
2026-01-01T22:33:58.491949500Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:33:58.491955845Z [err]      self._setup(name)
2026-01-01T22:33:58.491966177Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:33:58.491972817Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:33:58.491979664Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:58.491986214Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:33:58.491999854Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:33:59.586422353Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:59.586430181Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:33:59.586437208Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:33:59.586443984Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:33:59.586450352Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:33:59.586456475Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:33:59.586465967Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:33:59.586472146Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:33:59.586483009Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:33:59.586489319Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:33:59.586496646Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:33:59.586503350Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:34:00.829449061Z [err]                                                  ^^^^^
2026-01-01T22:34:00.829455639Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:19.000000000Z [inf]  Starting Container
2026-01-01T22:35:20.108106335Z [err]  Traceback (most recent call last):
2026-01-01T22:35:20.108116650Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:20.108122597Z [err]      main()
2026-01-01T22:35:20.108128281Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:20.108135939Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:20.108142393Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:20.108147420Z [err]      utility.execute()
2026-01-01T22:35:20.108154410Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:20.108159592Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:20.108165430Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:20.108170615Z [err]      self._setup(name)
2026-01-01T22:35:20.108175877Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:20.108180844Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:20.108186090Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:20.108191034Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:20.108196590Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:20.108788565Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:20.108800536Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:20.108806634Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:20.108811729Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:20.108816776Z [err]  ^^^^^^
2026-01-01T22:35:20.108822257Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:20.108827070Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:20.108831769Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:20.108836254Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:20.108841714Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:20.108846336Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:20.108851394Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:20.108855786Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:20.108892199Z [err]                                                  ^^^^^
2026-01-01T22:35:20.108897844Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:21.000000000Z [inf]  Stopping Container
2026-01-01T22:35:21.119506283Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:21.119509643Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:21.119516866Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:21.119522607Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:21.119529828Z [err]      utility.execute()
2026-01-01T22:35:21.119536399Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:21.119546081Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:21.119552089Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:21.119559242Z [err]      self._setup(name)
2026-01-01T22:35:21.119564803Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:21.119570946Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:21.119574364Z [err]  Traceback (most recent call last):
2026-01-01T22:35:21.119579159Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:21.119584670Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:21.119599262Z [err]      main()
2026-01-01T22:35:21.119607786Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:21.119873710Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:21.119885989Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:21.119895210Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:21.119903880Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:21.119912156Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:21.119920365Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:21.119928609Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:21.119937241Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:21.119947101Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:21.119955167Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:21.119963535Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:21.119971581Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:21.119981380Z [err]                                                  ^^^^^
2026-01-01T22:35:21.119989080Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:22.119729127Z [err]  Traceback (most recent call last):
2026-01-01T22:35:22.119734704Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:22.119741581Z [err]      main()
2026-01-01T22:35:22.119747144Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:22.119753559Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:22.119758719Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:22.119764616Z [err]      utility.execute()
2026-01-01T22:35:22.119770395Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:22.119775836Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:22.119780658Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:22.119785456Z [err]      self._setup(name)
2026-01-01T22:35:22.119790091Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:22.119794762Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:22.119800180Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:22.119805700Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:22.119810775Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:22.120170305Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:22.120176086Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:22.120181208Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:22.120185746Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:22.120190526Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:22.120195263Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:22.120199877Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:22.120204639Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:22.120209101Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:22.120217338Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:22.120221938Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:22.120226193Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:22.120407934Z [err]                                                  ^^^^^
2026-01-01T22:35:22.120414457Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:23.407168749Z [err]  Traceback (most recent call last):
2026-01-01T22:35:23.407178497Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:23.407184558Z [err]      main()
2026-01-01T22:35:23.407190751Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:23.407196331Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:23.407201923Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:23.407207198Z [err]      utility.execute()
2026-01-01T22:35:23.407214560Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:23.407220205Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:23.407225931Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:23.407231559Z [err]      self._setup(name)
2026-01-01T22:35:23.407236767Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:23.407243697Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:23.407251615Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:23.407259512Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:23.407266348Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:23.407829618Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:23.407837840Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:23.407842580Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:23.407846890Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:23.407851187Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:23.407855534Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:23.407859737Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:23.407864077Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:23.407868706Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:23.407873852Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:23.407878095Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:23.407882167Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:23.408414023Z [err]                                                  ^^^^^
2026-01-01T22:35:23.408423851Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:24.998912756Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:24.998913668Z [err]  Traceback (most recent call last):
2026-01-01T22:35:24.998927315Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:24.998930776Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:24.998935522Z [err]      main()
2026-01-01T22:35:24.998942615Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:24.998944976Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:24.998949011Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:24.998955364Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:24.998957666Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:24.998961784Z [err]      utility.execute()
2026-01-01T22:35:24.998967278Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:24.998972264Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:24.998977014Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:24.998981603Z [err]      self._setup(name)
2026-01-01T22:35:24.998986209Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:25.000479437Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:25.000487605Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:25.000493532Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:25.000498288Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:25.000503019Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:25.000508447Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:25.000513479Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:25.000518718Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:25.000523293Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:25.000528587Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:25.000533210Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:25.000537777Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:25.000659029Z [err]                                                  ^^^^^
2026-01-01T22:35:25.000667138Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:26.429222569Z [err]  Traceback (most recent call last):
2026-01-01T22:35:26.429230728Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:26.429238087Z [err]      main()
2026-01-01T22:35:26.429244463Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:26.429250355Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:26.429257789Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:26.429264569Z [err]      utility.execute()
2026-01-01T22:35:26.429270916Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:26.429278215Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:26.429301609Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:26.429311078Z [err]      self._setup(name)
2026-01-01T22:35:26.429318459Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:26.429328719Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:26.429336310Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:26.429343823Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:26.429350869Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:26.429956908Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:26.429965843Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:26.429971871Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:26.429977900Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:26.429983392Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:26.429990458Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:26.429998417Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:26.430005460Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:26.430012918Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:26.430020210Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:26.430027067Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:26.430034658Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:26.430184647Z [err]                                                  ^^^^^
2026-01-01T22:35:26.430192532Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:27.707511951Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:27.707525286Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:27.707533841Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:27.707544535Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:27.707553001Z [err]  Traceback (most recent call last):
2026-01-01T22:35:27.707561379Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:27.707579896Z [err]      main()
2026-01-01T22:35:27.707588356Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:27.707596381Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:27.707604591Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:27.707611820Z [err]      utility.execute()
2026-01-01T22:35:27.707617439Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:27.707622388Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:27.707629333Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:27.707634628Z [err]      self._setup(name)
2026-01-01T22:35:27.707639394Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:27.708359251Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:27.708365149Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:27.708370482Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:27.708376174Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:27.708381436Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:27.708386344Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:27.708391858Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:27.708399528Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:27.708405023Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:27.708410756Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:27.708415796Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:27.708421098Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:27.708426265Z [err]                                                  ^^^^^
2026-01-01T22:35:27.708545575Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:28.766685975Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:28.766691595Z [err]  Traceback (most recent call last):
2026-01-01T22:35:28.766698198Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:28.766701168Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:28.766707003Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:28.766708746Z [err]      main()
2026-01-01T22:35:28.766715421Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:28.766716462Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:28.766722933Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:28.766727943Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:28.766732398Z [err]      utility.execute()
2026-01-01T22:35:28.766736833Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:28.766741261Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:28.766745839Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:28.766750686Z [err]      self._setup(name)
2026-01-01T22:35:28.766755827Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:28.767229686Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:28.767237233Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:28.767244046Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:28.767248709Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:28.767253593Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:28.767258276Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:28.767263126Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:28.767267633Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:28.767273351Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:28.767278615Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:28.767283065Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:28.767287472Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:28.767573808Z [err]                                                  ^^^^^
2026-01-01T22:35:28.767585815Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:29.822389223Z [err]  Traceback (most recent call last):
2026-01-01T22:35:29.822395621Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:29.822400369Z [err]      main()
2026-01-01T22:35:29.822404823Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:29.822410036Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:29.822414607Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:29.822418877Z [err]      utility.execute()
2026-01-01T22:35:29.822423213Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:29.822427562Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:29.822432007Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:29.822437816Z [err]      self._setup(name)
2026-01-01T22:35:29.822442792Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:29.822447334Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:29.822452109Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:29.822456587Z [err]  ^^
2026-01-01T22:35:29.822460822Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:29.822465257Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:29.823256171Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:29.823262616Z [err]  ^^^
2026-01-01T22:35:29.823267726Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:29.823272301Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:29.823276816Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:29.823281381Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:29.823285726Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:29.823290024Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:29.823294534Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:29.823298989Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:29.823304811Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:29.823309011Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:29.823837163Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:29.823844578Z [err]                                                  ^^^^^
2026-01-01T22:35:29.823849653Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:31.107811342Z [err]  Traceback (most recent call last):
2026-01-01T22:35:31.107817254Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:31.107822650Z [err]      main()
2026-01-01T22:35:31.107828398Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:31.107834162Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:31.107839529Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:31.107844789Z [err]      utility.execute()
2026-01-01T22:35:31.107850252Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:31.107856910Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:31.107861985Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:31.107866784Z [err]      self._setup(name)
2026-01-01T22:35:31.107871937Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:31.107877099Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:31.107882079Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:31.107887444Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:31.107892012Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:31.111640025Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:31.111644962Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:31.111650925Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:31.111656026Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:31.111662129Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:31.111666538Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:31.111674551Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:31.111679576Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:31.111684833Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:31.111690005Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:31.111695400Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:31.111700115Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:31.111705179Z [err]                                                  ^^^^^
2026-01-01T22:35:31.111710222Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:35:32.457376403Z [err]  Traceback (most recent call last):
2026-01-01T22:35:32.457386458Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:35:32.457393332Z [err]      main()
2026-01-01T22:35:32.457401378Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:35:32.457411173Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:35:32.457417142Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:35:32.457422670Z [err]      utility.execute()
2026-01-01T22:35:32.457429398Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:35:32.457502233Z [err]      settings.INSTALLED_APPS
2026-01-01T22:35:32.457510865Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:35:32.457518330Z [err]      self._setup(name)
2026-01-01T22:35:32.457524803Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:35:32.457531100Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:35:32.457536094Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:32.457541373Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:35:32.457546916Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:35:32.461045466Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:32.461062195Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:35:32.461068771Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:35:32.461074322Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:35:32.461079860Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:35:32.461085250Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:35:32.461090459Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:35:32.461096748Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:35:32.461101932Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:35:32.461108909Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:35:32.461114220Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:35:32.461119192Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:35:32.461124412Z [err]                                                  ^^^^^
2026-01-01T22:35:32.461129236Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:37:58.000000000Z [inf]  Starting Container
2026-01-01T22:37:59.678270966Z [err]  Traceback (most recent call last):
2026-01-01T22:37:59.678276550Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:37:59.678280701Z [err]      main()
2026-01-01T22:37:59.678285619Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:37:59.678290201Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:37:59.678294983Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:37:59.678301213Z [err]      utility.execute()
2026-01-01T22:37:59.678306754Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:37:59.678312222Z [err]      settings.INSTALLED_APPS
2026-01-01T22:37:59.678316880Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:37:59.678320988Z [err]      self._setup(name)
2026-01-01T22:37:59.678325128Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:37:59.678330194Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:37:59.678337140Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:37:59.678342834Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:37:59.678348705Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:37:59.679170428Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:37:59.679184524Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:37:59.679260150Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:37:59.679271111Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:37:59.679277019Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:37:59.679282708Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:37:59.679291448Z [err]  ^^^^^^^^^^^^
2026-01-01T22:37:59.679297576Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:37:59.679304480Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:37:59.679311823Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:37:59.679319255Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:37:59.679326392Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:37:59.679332658Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:37:59.679591210Z [err]                                                  ^^^^^
2026-01-01T22:37:59.679597807Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:00.259604801Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:00.259608191Z [err]  Traceback (most recent call last):
2026-01-01T22:38:00.259613256Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:00.259614022Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:00.259618610Z [err]      main()
2026-01-01T22:38:00.259620942Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:00.259623877Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:00.259626749Z [err]      self._setup(name)
2026-01-01T22:38:00.259630644Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:00.259633944Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:00.259636271Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:00.259640286Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:00.259641779Z [err]      utility.execute()
2026-01-01T22:38:00.259645399Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:00.259649708Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:00.259655943Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:00.261508016Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:00.261530472Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:00.261538440Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:00.261543923Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:00.261549594Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:00.261555158Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:00.261560747Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:00.261566057Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:00.261571690Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:00.261577439Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:00.261583319Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:00.261588913Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:00.262451807Z [err]                                                  ^^^^^
2026-01-01T22:38:00.262457324Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:01.000000000Z [inf]  Stopping Container
2026-01-01T22:38:01.262953513Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:01.262955285Z [err]  Traceback (most recent call last):
2026-01-01T22:38:01.262969140Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:01.262974315Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:01.262980156Z [err]      main()
2026-01-01T22:38:01.262990625Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:01.262991349Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:01.263003868Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:01.263006176Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:01.263016058Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:01.263020737Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:01.263032942Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:01.263033382Z [err]      utility.execute()
2026-01-01T22:38:01.263042980Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:01.263049072Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:01.263055137Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:01.263061405Z [err]      self._setup(name)
2026-01-01T22:38:01.263067639Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:01.263424490Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:01.263432107Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:01.263437210Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:01.263442998Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:01.263447404Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:01.263451248Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:01.263455260Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:01.263459298Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:01.263463153Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:01.263467709Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:01.263471406Z [err]                                                  ^^^^^
2026-01-01T22:38:01.263475712Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:02.246838746Z [err]  Traceback (most recent call last):
2026-01-01T22:38:02.246843548Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:02.246848110Z [err]      main()
2026-01-01T22:38:02.246852733Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:02.246856801Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:02.246864454Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:02.246876271Z [err]      utility.execute()
2026-01-01T22:38:02.246884016Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:02.246889951Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:02.246895906Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:02.246901445Z [err]      self._setup(name)
2026-01-01T22:38:02.246906862Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:02.246912819Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:02.246920289Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:02.246927091Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:02.246934016Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:02.247724706Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:02.247724736Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:02.247732582Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:02.247739214Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:02.247744548Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:02.247749950Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:02.247755327Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:02.247760512Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:02.247765507Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:02.247770840Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:02.247776155Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:02.247781247Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:02.247786476Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:02.247791739Z [err]                                                  ^^^^^
2026-01-01T22:38:03.225507270Z [err]  Traceback (most recent call last):
2026-01-01T22:38:03.225512875Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:03.225517406Z [err]      main()
2026-01-01T22:38:03.225521940Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:03.225527858Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:03.225533113Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:03.227594778Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:03.227601311Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:03.227601803Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:03.227607909Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:03.227610853Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:03.227616568Z [err]      utility.execute()
2026-01-01T22:38:03.227617236Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:03.227618253Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:03.227623507Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:03.227626577Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:03.227627668Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:03.227633529Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:03.227634725Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:03.227640341Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:03.227642568Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:03.227646847Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:03.227651778Z [err]      self._setup(name)
2026-01-01T22:38:03.227652739Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:03.228267341Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:03.228271237Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:03.228275452Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:03.228279729Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:03.228285917Z [err]                                                  ^^^^^
2026-01-01T22:38:03.228290188Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:04.153153656Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:04.153168326Z [err]  Traceback (most recent call last):
2026-01-01T22:38:04.153172534Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:04.153177513Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:04.153185553Z [err]      main()
2026-01-01T22:38:04.153189461Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:04.153195162Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:04.153200532Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:04.153206471Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:04.153211413Z [err]      utility.execute()
2026-01-01T22:38:04.153217778Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:04.153223524Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:04.153228458Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:04.153233712Z [err]      self._setup(name)
2026-01-01T22:38:04.153238248Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:04.153243182Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:04.153943315Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:04.153950040Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:04.153954745Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:04.153958938Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:04.153962891Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:04.153967083Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:04.153970747Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:04.153975073Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:04.153978602Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:04.153982450Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:04.153986296Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:04.153991492Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:04.154554143Z [err]                                                  ^^^^^
2026-01-01T22:38:04.154560307Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:05.105874246Z [err]  Traceback (most recent call last):
2026-01-01T22:38:05.105890307Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:05.105900726Z [err]      main()
2026-01-01T22:38:05.105909867Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:05.105917259Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:05.105925345Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:05.105932799Z [err]      utility.execute()
2026-01-01T22:38:05.105939996Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:05.105946703Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:05.105954623Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:05.105963773Z [err]      self._setup(name)
2026-01-01T22:38:05.105971381Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:05.105977141Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:05.105983787Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:05.105989983Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:05.105997114Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:05.106518954Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:05.106525046Z [err]  ^^^^^^^
2026-01-01T22:38:05.106530725Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:05.106536507Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:05.106542397Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:05.106547383Z [err]  ^^^^^^^^^^^
2026-01-01T22:38:05.106553039Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:05.106557639Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:05.106562815Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:05.106568053Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:05.106573733Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:05.106578380Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:05.107052846Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:05.107060987Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:05.107066659Z [err]                                           
2026-01-01T22:38:05.107073272Z [err]         ^^^^^
2026-01-01T22:38:05.107079452Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:06.020103575Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:06.020110684Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:06.020112354Z [err]      utility.execute()
2026-01-01T22:38:06.020119369Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:06.020120136Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:06.020126761Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.020127383Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:06.020129355Z [err]  Traceback (most recent call last):
2026-01-01T22:38:06.020136232Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:06.020136912Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:06.020138112Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:06.020143231Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:06.020146215Z [err]      self._setup(name)
2026-01-01T22:38:06.020146387Z [err]      main()
2026-01-01T22:38:06.020153183Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:06.020158940Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:06.020821254Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.020831900Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:06.020837506Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:06.020842481Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.020848010Z [err]  ^^^^^^^^^^^^
2026-01-01T22:38:06.020856603Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:06.020861963Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:06.020867258Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:06.020872228Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:06.020877705Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:06.020882623Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:06.020886625Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:06.020892047Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:06.021232861Z [err]                                                  ^^^^^
2026-01-01T22:38:06.021239227Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:06.876009775Z [err]  Traceback (most recent call last):
2026-01-01T22:38:06.876014260Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:06.876020959Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:06.876026142Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:06.876029670Z [err]      main()
2026-01-01T22:38:06.876035379Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:06.876037139Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:06.876043183Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:06.876044050Z [err]      self._setup(name)
2026-01-01T22:38:06.876050060Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:06.876053039Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:06.876057384Z [err]      utility.execute()
2026-01-01T22:38:06.876061874Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:06.876068680Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.876075936Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:06.876083577Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:06.877156777Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.877162455Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:06.877166646Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:06.877170428Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:06.877174186Z [err]  
2026-01-01T22:38:06.877178226Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:06.877182007Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:06.877185456Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:06.877189146Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:06.877192996Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:06.877196608Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:06.877200385Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:06.877203777Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:06.877999424Z [err]                                                  ^^^^^
2026-01-01T22:38:06.878003903Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:07.946692254Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:07.946701037Z [err]      self._setup(name)
2026-01-01T22:38:07.946712830Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:07.946717553Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:07.946721936Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:07.946726389Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:07.946731304Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:07.946926514Z [err]  Traceback (most recent call last):
2026-01-01T22:38:07.946934887Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:07.946939347Z [err]      main()
2026-01-01T22:38:07.946943254Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:07.946947832Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:07.946951985Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:07.946956155Z [err]      utility.execute()
2026-01-01T22:38:07.946959942Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:07.946964137Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:07.947680075Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:07.947685090Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:07.947689161Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:07.947692787Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:07.947696369Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:07.947700085Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:07.947704510Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:07.947708740Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:07.947712561Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:38:07.947713402Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:07.947717847Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:07.947722013Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:07.947725714Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:07.947729514Z [err]                                                  ^^^^^
2026-01-01T22:38:08.920847719Z [err]      self._setup(name)
2026-01-01T22:38:08.920862236Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 76, in _setup
2026-01-01T22:38:08.920871016Z [err]      self._wrapped = Settings(settings_module)
2026-01-01T22:38:08.920871156Z [err]  Traceback (most recent call last):
2026-01-01T22:38:08.920876839Z [err]    File "/app/manage.py", line 29, in <module>
2026-01-01T22:38:08.920878192Z [err]                      ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:08.920885156Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 190, in __init__
2026-01-01T22:38:08.920887629Z [err]      main()
2026-01-01T22:38:08.920894555Z [err]      mod = importlib.import_module(self.SETTINGS_MODULE)
2026-01-01T22:38:08.920896425Z [err]    File "/app/manage.py", line 25, in main
2026-01-01T22:38:08.920901310Z [err]      execute_from_command_line(sys.argv)
2026-01-01T22:38:08.920905446Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2026-01-01T22:38:08.920909143Z [err]      utility.execute()
2026-01-01T22:38:08.920913129Z [err]    File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
2026-01-01T22:38:08.920917355Z [err]      settings.INSTALLED_APPS
2026-01-01T22:38:08.920921584Z [err]    File "/usr/local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in __getattr__
2026-01-01T22:38:08.923341008Z [err]    File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-01-01T22:38:08.923349280Z [err]    File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-01-01T22:38:08.923353109Z [err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:08.923358445Z [err]    File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-01-01T22:38:08.923360485Z [err]    File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-01-01T22:38:08.923365004Z [err]    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-01-01T22:38:08.923365776Z [err]      return _bootstrap._gcd_import(name[level:], package, level)
2026-01-01T22:38:08.923370635Z [err]    File "/app/config/settings.py", line 21, in <module>
2026-01-01T22:38:08.923370730Z [err]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-01-01T22:38:08.923376646Z [err]    File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-01-01T22:38:08.923376843Z [err]      if not os.environ.get('SECRET_KEY') and not DEBUG:
2026-01-01T22:38:08.923381456Z [err]    File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-01-01T22:38:08.925447709Z [err]                                                  ^^^^^
2026-01-01T22:38:08.925458023Z [err]  NameError: name 'DEBUG' is not defined
2026-01-01T22:43:38.000000000Z [inf]  Starting Container
2026-01-01T22:43:41.000000000Z [inf]  Stopping Container
2026-01-01T22:43:41.041742687Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T22:46:23.000000000Z [inf]  Starting Container
2026-01-01T22:46:24.945417016Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T22:46:26.000000000Z [inf]  Stopping Container
2026-01-01T22:54:04.000000000Z [inf]  Starting Container
2026-01-01T22:54:06.602372925Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T22:54:08.000000000Z [inf]  Stopping Container
2026-01-01T22:59:50.000000000Z [inf]  Starting Container
2026-01-01T22:59:53.000000000Z [inf]  Stopping Container
2026-01-01T22:59:53.270553356Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T23:19:21.000000000Z [inf]  Starting Container
2026-01-01T23:19:23.275854384Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T23:19:24.000000000Z [inf]  Stopping Container
2026-01-01T23:26:01.000000000Z [inf]  Starting Container
2026-01-01T23:26:03.363085347Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-01T23:26:04.000000000Z [inf]  Stopping Container
2026-01-02T00:32:47.000000000Z [inf]  Starting Container
2026-01-02T00:32:49.280678520Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T00:32:50.000000000Z [inf]  Stopping Container
2026-01-02T00:34:03.000000000Z [inf]  Starting Container
2026-01-02T00:34:05.253143838Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T00:34:06.000000000Z [inf]  Stopping Container
2026-01-02T00:38:56.000000000Z [inf]  Starting Container
2026-01-02T00:38:58.942493106Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T00:39:00.000000000Z [inf]  Stopping Container
2026-01-02T00:42:09.000000000Z [inf]  Starting Container
2026-01-02T00:42:12.000000000Z [inf]  Stopping Container
2026-01-02T00:42:12.318079482Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T00:42:29.000000000Z [inf]  Starting Container
2026-01-02T00:42:31.961345777Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T00:42:32.000000000Z [inf]  Stopping Container
2026-01-02T13:14:46.728859778Z [err]  2026-01-02 13:14:42.111 UTC [32314] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728865859Z [err]  2026-01-02 13:14:42.618 UTC [32316] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728870800Z [err]  2026-01-02 13:14:43.126 UTC [32317] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728875511Z [err]  2026-01-02 13:14:43.474 UTC [32318] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728879835Z [err]  2026-01-02 13:14:43.823 UTC [32319] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728884103Z [err]  2026-01-02 13:14:44.170 UTC [32320] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728889222Z [err]  2026-01-02 13:14:44.678 UTC [32321] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728894703Z [err]  2026-01-02 13:14:45.027 UTC [32322] LOG:  invalid length of startup packet
2026-01-02T13:14:46.728899318Z [err]  2026-01-02 13:14:45.535 UTC [32323] LOG:  could not accept SSL connection: version too low
2026-01-02T13:14:46.728910376Z [err]  2026-01-02 13:14:45.535 UTC [32323] HINT:  This may indicate that the client does not support any SSL protocol version between TLSv1.2 and TLSv1.3.
2026-01-02T13:14:46.728916459Z [err]  2026-01-02 13:14:46.229 UTC [32324] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:46.944012092Z [err]  2026-01-02 13:14:46.924 UTC [32325] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:47.751861436Z [err]  2026-01-02 13:14:47.620 UTC [32326] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:48.720459130Z [err]  2026-01-02 13:14:48.315 UTC [32327] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:49.767012543Z [err]  2026-01-02 13:14:49.008 UTC [32328] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:49.767020245Z [err]  2026-01-02 13:14:49.703 UTC [32329] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:50.825059038Z [err]  2026-01-02 13:14:50.398 UTC [32330] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:51.676267767Z [err]  2026-01-02 13:14:51.091 UTC [32331] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:51.797498053Z [err]  2026-01-02 13:14:51.784 UTC [32332] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:52.871434525Z [err]  2026-01-02 13:14:52.477 UTC [32333] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:53.807014363Z [err]  2026-01-02 13:14:53.175 UTC [32334] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:53.880417124Z [err]  2026-01-02 13:14:53.868 UTC [32335] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:54.698509621Z [err]  2026-01-02 13:14:54.561 UTC [32336] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:55.751517053Z [err]  2026-01-02 13:14:55.258 UTC [32337] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:55.956497289Z [err]  2026-01-02 13:14:55.952 UTC [32338] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:56.873982834Z [err]  2026-01-02 13:14:56.646 UTC [32339] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:58.097677125Z [err]  2026-01-02 13:14:57.341 UTC [32340] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:58.097683061Z [err]  2026-01-02 13:14:58.036 UTC [32341] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:14:59.191657129Z [err]  2026-01-02 13:14:58.730 UTC [32342] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:00.330080487Z [err]  2026-01-02 13:14:59.423 UTC [32343] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:00.330091339Z [err]  2026-01-02 13:15:00.119 UTC [32345] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:01.512771472Z [err]  2026-01-02 13:15:00.813 UTC [32346] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:02.433366662Z [err]  2026-01-02 13:15:01.512 UTC [32347] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:02.433372894Z [err]  2026-01-02 13:15:02.207 UTC [32348] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:03.293928125Z [err]  2026-01-02 13:15:02.901 UTC [32349] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:04.412944388Z [err]  2026-01-02 13:15:03.596 UTC [32350] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:04.412951338Z [err]  2026-01-02 13:15:04.290 UTC [32351] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:05.586597917Z [err]  2026-01-02 13:15:04.983 UTC [32352] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:06.487760557Z [err]  2026-01-02 13:15:05.680 UTC [32353] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:15:06.487768902Z [err]  2026-01-02 13:15:06.380 UTC [32354] LOG:  received direct SSL connection request without ALPN protocol negotiation extension
2026-01-02T13:33:48.000000000Z [inf]  Starting Container
2026-01-02T13:33:50.000000000Z [inf]  Stopping Container
2026-01-02T13:33:50.291291979Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T14:17:46.000000000Z [inf]  Starting Container
2026-01-02T14:17:47.896457682Z [inf]  ADMIN_PASSWORD not set in environment. Skipping admin creation.
2026-01-02T14:17:49.000000000Z [inf]  Stopping Container