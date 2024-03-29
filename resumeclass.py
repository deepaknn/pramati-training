from tika import parser
import re
import psycopg2
import pysolr
import os

class RParser:
	def __init__(self):
		self.email = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
		self.phone = "[0-9]{10}"
		self.languages=['HTML', 'CSS', 'Android', 'SQL', 'MySql', 'Angular js2', 'Ajax', 'xampp', 'A\\# \\.NET',
                  'A\\#', 'A-0', 'A\\+', 'A\\+\\+', 'ABAP', 'ABC', 'ABC ALGOL', 'ABSET', 'ABSYS', 'ACC',
                  'Accent', 'Ace DASL', 'ACL2', 'ACT-III', 'Action\\!', 'ActionScript', 'Ada', 'Adenine',
                  'Agda', 'Agilent VEE', 'Agora', 'AIMMS', 'Alef', 'ALF', 'ALGOL 58', 'ALGOL 60', 'ALGOL 68',
                  'ALGOL W', 'Alice', 'Alma-0', 'AmbientTalk', 'Amiga E', 'AMOS', 'AMPL', 'Apex', 'APL', 'App',
                  'AppleScript', 'Arc', 'ARexx', 'Argus', 'AspectJ', 'Assembly language', 'ATS', 'Ateji PX',
                  'AutoHotkey', 'Autocoder', 'AutoIt', 'AutoLISP / Visual LISP', 'Averest', 'AWK', 'Axum', 'B',
                  'Babbage', 'Bash', 'BASIC', 'bc', 'BCPL', 'BeanShell', 'Batch ', 'Bertrand', 'BETA', 'Bigwig',
                  'Bistro', 'BitC', 'BLISS', 'Blockly', 'BlooP', 'Blue', 'Boo', 'Boomerang', 'Bourne shell',
                  'BREW', 'BPEL', 'C', 'C--', 'C\\+\\+', 'C\\#', 'C\\/AL', 'Cache ObjectScript', 'C Shell',
                  'Caml', 'Cayenne', 'CDuce', 'Cecil', 'Cel', 'Cesil', 'Ceylon', 'CFEngine', 'CFML', 'Cg', 'Ch',
                  'Chapel', 'CHAIN', 'Charity', 'Charm', 'Chef', 'CHILL', 'CHIP-8', 'chomski', 'ChucK', 'CICS',
                  'Cilk', 'Citrine ', 'CL ', 'Claire', 'Clarion', 'Clean', 'Clipper', 'CLIST', 'Clojure', 'CLU',
                  'CMS-2', 'COBOL', 'Cobra', 'CODE', 'CoffeeScript', 'ColdFusion', 'COMAL',
                  'Combined Programming Language ', 'COMIT', 'Common Intermediate Language ', 'Common Lisp ',
                  'COMPASS', 'Component Pascal', 'Constraint Handling Rules ', 'Converge', 'Cool', 'Coq',
                  'Coral 66', 'Corn', 'CorVision', 'COWSEL', 'CPL', 'Cryptol', 'csh', 'Csound', 'CSP', 'CUDA',
                  'Curl', 'Curry', 'Cyclone', 'Cython', 'D', 'DASL ', 'DASL ', 'Dart', 'DataFlex', 'Datalog',
                  'DATATRIEVE', 'dBase', 'dc', 'DCL', 'Deesel ', 'Delphi', 'DinkC', 'DIBOL', 'Dog', 'Draco',
                  'DRAKON', 'Dylan', 'DYNAMO', 'E', 'E\\#', 'Ease', 'Easy PL/I', 'Easy Programming Language',
                  'EASYTRIEVE PLUS', 'ECMAScript', 'Edinburgh IMP', 'EGL', 'Eiffel', 'ELAN', 'Elixir', 'Elm',
                  'Emacs Lisp', 'Emerald', 'Epigram', 'EPL', 'Erlang', 'es', 'Escher', 'ESPOL', 'Esterel',
                  'Etoys', 'Euclid', 'Euler', 'Euphoria', 'EusLisp', 'CMS EXEC ', 'EXEC 2', 'Executable UML',
                  'F', 'F\\#', 'Factor', 'Falcon', 'Fantom', 'FAUST', 'FFP', 'Fjolnir', 'FL', 'Flavors', 'Flex',
                  'FlooP', 'FLOW-MATIC', 'FOCAL', 'FOCUS', 'FOIL', 'FORMAC', '\\@Formula', 'Forth', 'Fortran',
                  'Fortress', 'FoxBase', 'FoxPro', 'FP', 'FPr', 'Franz Lisp', 'Frege', 'F-Script', 'G',
                  'Game Maker Language', 'GameMonkey Script', 'GAMS', 'GAP', 'G-code', 'Genie', 'GDL', 'GJ',
                  'GEORGE', 'GLSL', 'GNU E', 'GM', 'Go', 'Go\\!', 'GOAL', 'Godiva', 'Golo', 'GOM ',
                  'Google Apps Script', 'Gosu', 'GOTRAN', 'GPSS', 'GraphTalk', 'GRASS', 'Groovy', 'Hack',
                  'HAL/S', 'Hamilton C shell', 'Harbour', 'Hartmann pipelines', 'Haskell', 'Haxe',
                  'High Level Assembly', 'HLSL', 'Hop', 'Hopscotch', 'Hope', 'Hugo', 'Hume', 'HyperTalk',
                  'IBM Basic assembly language', 'IBM HAScript', 'IBM Informix-4GL', 'IBM RPG', 'ICI', 'Icon',
                  'Id', 'IDL', 'Idris', 'IMP', 'Inform', 'Io', 'Ioke', 'IPL', 'IPTSCRAE', 'ISLISP', 'ISPF',
                  'ISWIM', 'J', 'J\\#', 'J\\+\\+', 'JADE', 'Jako', 'JAL', 'Janus ', 'Janus ', 'JASS', 'Java',
                  'JavaScript', 'JCL', 'JEAN', 'Join Java', 'JOSS', 'Joule', 'JOVIAL', 'Joy', 'JScript',
                  'JScript \\.NET', 'JavaFX Script', 'Julia', 'Jython', 'K', 'Kaleidoscope', 'Karel',
                  'Karel\\+\\+', 'KEE', 'Kixtart', 'Klerer-May', 'KIF', 'Kojo', 'Kotlin', 'KRC', 'KRL', 'KUKA',
                  'KRYPTON', 'ksh', 'L', 'L\\# \\.NET', 'LabVIEW', 'Ladder', 'Lagoona', 'LANSA', 'Lasso',
                  'LaTeX', 'Lava', 'LC-3', 'Leda', 'Legoscript', 'LIL', 'LilyPond', 'Limbo', 'Limnor', 'LINC',
                  'Lingo', 'LIS', 'LISA', 'Lisaac', 'Lisp', 'Lite-C', 'Lithe', 'Little b', 'Logo', 'Logtalk',
                  'LotusScript', 'LPC', 'LSE', 'LSL', 'LiveCode', 'LiveScript', 'Lua', 'Lucid', 'Lustre',
                  'LYaPAS', 'Lynx', 'M2001', 'MarsCode ', 'M4', 'M\\#', 'Machine code', 'MAD ', 'MAD\\/I',
                  'Magik', 'Magma', 'make', 'Maple', 'MAPPER', 'MARK-IV', 'Mary', 'MASM', 'MATH-MATIC',
                  'Mathematica', 'MATLAB', 'Maxima', 'Max ', 'MaxScript', 'Maya ', 'MDL', 'Mercury', 'Mesa',
                  'Metacard', 'Metafont', 'Microcode', 'MicroScript', 'MIIS', 'MillScript', 'MIMIC', 'Mirah',
                  'Miranda', 'MIVA Script', 'ML', 'Moby', 'Model 204', 'Modelica', 'Modula', 'Modula-2',
                  'Modula-3', 'Mohol', 'MOO', 'Mortran', 'Mouse', 'MPD', 'CIL', 'MSL', 'MUMPS', 'Mystic',
                  'NASM', 'Napier88', 'Neko', 'Nemerle', 'nesC', 'NESL', 'Net\\.Data', 'NetLogo', 'NetRexx',
                  'NewLISP', 'NEWP', 'Newspeak', 'NewtonScript', 'NGL', 'Nial', 'Nice', 'Nickle', 'Nim', 'NPL',
                  'Not eXactly C ', 'Not Quite C ', 'NSIS', 'Nu', 'NWScript', 'NXT-G', 'o\\:XML', 'Oak',
                  'Oberon', 'OBJ2', 'Object Lisp', 'ObjectLOGO', 'Object REXX', 'Object Pascal', 'Objective-C',
                  'Objective-J', 'Obliq', 'OCaml', 'occam', 'Octave', 'OmniMark', 'Onyx', 'Opa',
                  'Opal', 'OpenCL', 'OpenEdge ABL', 'OPL', 'OPS5', 'OptimJ', 'Orc', 'ORCA/Modula-2', 'Oriel',
                  'Orwell', 'Oxygene', 'Oz',  'P\\#', 'ParaSail ', 'PARI/GP', 'Pascal', 'PCASTL',
                  'PCF', 'PEARL', 'PeopleCode', 'Perl', 'PDL', 'Perl6', 'Pharo', 'PHP', 'Phrogram', 'Pico',
                  'Picolisp', 'Pict', 'Pike', 'PIKT', 'PILOT', 'Pipelines', 'Pizza', 'PL-11', 'PL/0', 'PL/B',
                  'PL/C',  'PL/M', 'PL/P', 'PL/SQL', 'PL360', 'PLANC',
                  'Planner', 'PLEX', 'PLEXIL', 'Plus', 'POP-11', 'PostScript', 'PortablE', 'Powerhouse',
                  'PowerBuilder', 'PowerShell', 'PPL', 'Processing', 'Processing\\.js', 'Prograph', 'PROIV',
                  'Prolog', 'PROMAL', 'Promela', 'PROSE modeling language', 'PROTEL', 'ProvideX', 'Pro\\*C',
                  'Pure', 'Python', 'Q ', 'Q ', 'Qalb', 'QtScript', 'QuakeC', 'QPL', 'R', 'R\\+\\+', 'Racket',
                  'RAPID', 'Rapira', 'Ratfiv', 'Ratfor', 'rc', 'REBOL', 'Red', 'Redcode', 'REFAL', 'Reia',
                  'Revolution', 'REXX', 'Rlab', 'ROOP', 'RPG', 'RPL', 'RSL', 'RTL/2', 'Ruby', 'RuneScript',
                  'Rust', 'S', 'S2', 'S3', 'S-Lang', 'S-PLUS', 'SA-C', 'SabreTalk', 'SAIL', 'SALSA', 'SAM76',
                  'SAS', 'SASL', 'Sather', 'Sawzall', 'SBL', 'Scala', 'Scheme', 'Scilab', 'Scratch',
                  'Script\\.NET', 'Sed', 'Seed7', 'Self', 'SenseTalk', 'SequenceL', 'SETL', 'SIMPOL', 'SIGNAL',
                  'SiMPLE', 'SIMSCRIPT', 'Simula', 'Simulink', 'SISAL', 'SLIP', 'SMALL', 'Smalltalk',
                  'Small Basic', 'SML', 'Snap\\!', 'SNOBOL', 'Snowball', 'SOL', 'Span', 'SPARK', 'Speedcode',
                  'SPIN', 'SP/k', 'SPS', 'SQR', 'Squeak', 'Squirrel', 'SR', 'S/SL', 'Stackless Python',
                  'Starlogo', 'Strand', 'Stata', 'Stateflow', 'Subtext', 'SuperCollider', 'SuperTalk', 'Swift ',
                  'Swift ', 'SYMPL', 'SyncCharts', 'SystemVerilog', 'T', 'TACL', 'TACPOL', 'TADS', 'TAL', 'Tcl',
                  'Tea', 'TECO', 'TELCOMP', 'TeX', 'TEX', 'TIE', 'Timber', '\\"TMG ', 'Tom', 'TOM',
                  'TouchDevelop', 'Topspeed', 'TPU', 'Trac', 'TTM', 'T-SQL', 'TTCN', 'Turing', 'TUTOR', 'TXL',
                  'TypeScript', 'Turbo C\\+\\+', 'Ubercode', 'UCSD Pascal', 'Umple', 'Unicon', 'Uniface',
                  'UNITY', 'Unix shell', 'UnrealScript', 'Vala', 'Visual DataFlex', 'Visual DialogScript',
                  'Visual Fortran', 'Visual FoxPro', 'Visual J\\+\\+', 'Visual J\\#', 'Visual Objects',
                  'Visual Prolog', 'VSXu', 'vvvv', '\\"WATFIV', 'WebDNA', 'WebQL', 'Whiley',
                  'Windows PowerShell', 'Winbatch', 'Wolfram Language', 'Wyvern', 'X\\+\\+', 'X\\#', 'X10',
                  'XBL', 'XC', 'xHarbour', 'XL', 'Xojo', 'XOTcl', 'XPL', 'XPL0', 'XQuery', 'XSB', 'XSLT',
                  'XPath', 'Xtend', 'Yorick', 'YQL', 'Z notation', 'Zeno', 'ZOPL', 'Zsh', 'ZPL','shell']
		self.CONNECTION = psycopg2.connect(user="postgres",password="docker",host="127.0.0.1",port="5432",database="postgres")
		self.CURSOR = self.CONNECTION.cursor()
		self.insert = "insert into resume values(%s,%s,%s,%s);"
		self.display = "select * from resume;"
		self.solr = pysolr.Solr('http://localhost:8983/solr/resumeparser/',timeout=10)

	def Data(self, path):
		text = parser.from_file(path)["content"]
		skills = []
		phonelist = re.findall(self.phone, text)
		emaillist = re.findall(self.email, text)
		for i in self.languages:
			temp_data = re.findall(re.compile('^(' + i + ')$| ^(' + i + ',) | (' + i + ')[,\\s]', re.IGNORECASE), text)
			if len(temp_data) >= 1 and temp_data[0] not in skills:
				skills.append(temp_data[0][2])
		return (str(emaillist[0]), str(phonelist[0]), skills, re.sub('\s+', ' ', text))


	def Push(self, values):
		try:
			self.CURSOR.execute(self.insert, values)
			self.CONNECTION.commit()
		except psycopg2.Error as error:
			print(error)

	def Retrieve(self):
		self.CURSOR.execute(self.display)
		print(self.CURSOR.fetchall())
	def Tojson(self, text):
		d={"email":text[0],"phone":text[1],"skills":text[2],"content":text[3]}
		return d
	def AddToSolr(self, data):
		self.solr.add([data])
		self.solr.commit()
	def SearchSolr(self, query):
		for i in self.solr.search(query):
			print(i)
if __name__ == "__main__":
	resume = RParser()
	path='/home/deepaknn/Downloads/resumes/'
	for filename in os.listdir(path):
		#resume.Push(resume.Data('/home/deepaknn/Downloads/Deepak_Resume.docx'))
		#resume.Retrieve()
		j=resume.Tojson(resume.Data(path+filename))
		print(j)
		resume.AddToSolr(j)
		resume.SearchSolr("skills:HTML")


