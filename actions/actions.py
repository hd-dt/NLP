# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType, SlotSet, AllSlotsReset

class ValidateDinoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_dino_form"

    def dino_names_db(self) -> List[Text]:
        #dino_names_org = pd.read_csv("C:/Users/hddt/NLP/data/dino_names_ls.csv")
        dino_names_org = ['Aachenosaurus','Aardonyx','Abelisaurus','Abrictosaurus','Abrosaurus','Abydosaurus','Acanthopholis','Achelousaurus','Acheroraptor','Achillesaurus','Achillobator','Acristavus','Acrocanthosaurus','Acrotholus','Adamantisaurus','Adasaurus','Adeopapposaurus','Adynomosaurus','Aegyptosaurus','Aeolosaurus','Aepisaurus','Aerodactylus','Aerosteon','Aerotitan','Aetodactylus','Aetonyx','Afrovenator','Agathaumas','Agilisaurus','Agnosphitys','Agrosaurus','Agujaceratops','Agustinia','Ahshislepelta','Airakoraptor','Ajancingenia','Ajkaceratops','Akainacephalus','Alamosaurus','Alanqa','Alaskacephale','Albalophosaurus','Albertaceratops','Albertadromeus','Albertonectes','Albertonykus','Albertosaurus','Albinykus','Alcovasaurus','Alectrosaurus','Aletopelta','Alexeyisaurus','Algoasaurus','Alioramus','Allosaurus','Alnashetri','Alocodon','Altirhinus','Altispinax','Alvarezsaurus','Alwalkeria','Alxasaurus','Amargasaurus','Amargatitanis','Amazonsaurus','Ammosaurus','Ampelosaurus','Amphicoelias','Amtocephale','Amtosaurus','Amurosaurus','Amygdalodon','Anabisetia','Anasazisaurus','Anatotitan','Anchiceratops','Anchiornis','Anchisaurus','Andesaurus','Angaturama','Angloposeidon','Angolatitan','Angulomastacator','Angustinaripterus','Anhanguera','Aniksosaurus','Animantarx','Ankylosaurus','Anningasaura','Anodontosaurus','Anoplosaurus','Anserimimus','Antarctopelta','Antarctosaurus','Antetonitrus','Antrodemus','Anurognathus','Anzu','Aoniraptor','Aorun','Apatodon','Apatomerus','Apatosaurus','Aphrosaurus','Appalachiosaurus','Aquilarhinus','Aragosaurus','Aralazhdarcho','Aralosaurus','Arambourgiania','Araripesaurus','Archaeoceratops','Archaeodontosaurus','Archaeoistiodactylus','Archaeonectrus','Archaeopteryx','Archaeornithoides','Archaeornithomimus','Arcovenator','Arcusaurus','Ardeadactylus','Arenysaurus','Argentinosaurus','Argyrosaurus','Aristonectes','Aristosuchus','Arkansaurus','Arkharavia','Arrhinoceratops','Arstanosaurus','Arthurdactylus','Asiaceratops','Asiatosaurus','Astrodon','Astrophocaudia','Asylosaurus','Atacamatitan','Atlantosaurus','Atlasaurus','Atlascopcosaurus','Atrociraptor','Atsinganosaurus','Attenborosaurus','Aublysodon','Aucasaurus','Augustasaurus','Augustynolophus','Auroraceratops','Aurorazhdarcho','Aurornis','Australodocus','Australovenator','Austriadactylus','Austrocheirus','Austroraptor','Austrosaurus','Avaceratops','Aviatyrannis','Avimimus','Avipes','Azhdarcho','Bactrosaurus','Bagaceratops','Bagaraatan','Bahariasaurus','Bainoceratops','Bakonydraco','Balaur','Balochisaurus','Bambiraptor','Banji','Baotianmansaurus','Barapasaurus','Barbosania','Barilium','Barosaurus','Barrosasaurus','Barsboldia','Baryonyx','Batrachognathus','Batyrosaurus','Baurutitan','Bayosaurus','Becklespinax','Beelemodon','Beipiaopterus','Beipiaosaurus','Beishanlong','Bellubrunnus','Bellusaurus','Berberosaurus','Betasuchus','Bicentenaria','Bienosaurus','Bihariosaurus','Bishanopliosaurus','Bissektipelta','Bistahieversor','Blasisaurus','Blikanasaurus','Bobosaurus','Bolong','Bonapartenykus','Bonatitan','Bonitasaura','Borealosaurus','Boreopterus','Borogovia','Bothriospondylus','Brachauchenius','Brachiosaurus','Brachyceratops','Brachylophosaurus','Brachytrachelopan','Bradycneme','Brancasaurus','Brasileodactylus','Brasilotitan','Bravoceratops','Breviceratops','Brohisaurus','Brontomerus','Brontosaurus','Bruhathkayosaurus','Buitreraptor','Burianosaurus','Byronosaurus','Cacibupteryx','Caenagnathasia','Caiuajara','Calamosaurus','Calamospondylus','Callawayasaurus','Callovosaurus','Camarasaurus','Camarillasaurus','Camelotia','Camposaurus','Camptosaurus','Campylodoniscus','Campylognathoides','Canardia','Capitalsaurus','Carcharodontosaurus','Cardiodon','Carniadactylus','Carnotaurus','Caseosaurus','Cathartesaura','Cathetosaurus','Caudipteryx','Caulkicephalus','Caviramus','Cearadactylus','Cedarosaurus','Cedarpelta','Cedrorestes','Centrosaurus','Cerasinops','Ceratonykus','Ceratops','Ceratosaurus','Cetiosauriscus','Cetiosaurus','Changchengopterus','Changchunsaurus','Changdusaurus','Changyuraptor','Chaoyangopterus','Chaoyangsaurus','Charonosaurus','Chasmosaurus','Chebsaurus','Chenanisaurus','Chialingosaurus','Chilantaisaurus','Chilesaurus','Chindesaurus','Chingkankousaurus','Chinshakiangosaurus','Chirostenotes','Chondrosteosaurus','Choyrodon','Chromogisaurus','Chuandongocoelurus','Chuanjiesaurus','Chuanqilong','Chubutisaurus','Chungkingosaurus','Chuxiongosaurus','Cionodon','Citipati','Claorhynchus','Claosaurus','Clasmodosaurus','Coahuilaceratops','Coelophysis','Coeluroides','Coelurus','Colepiocephale','Coloborhynchus','Coloradisaurus','Colymbosaurus','Comahuesaurus','Comanchesaurus','Compsognathus','Compsosuchus','Concavenator','Conchoraptor','Condorraptor','Confuciusornis','Coronosaurus','Corythosaurus','Craspedodon','Craterosaurus','Crichtonpelta','Crichtonsaurus','Criorhynchus','Cristatusaurus','Cruxicheiros','Cryolophosaurus','Cryptocleidus','Cryptoclidus','Cryptosaurus','Cryptovolans','Ctenochasma','Cumnoria','Cuspicephalus','Cycnorhamphus','Cymatosaurus','Daanosaurus','Dacentrurus','Dachongosaurus','Daemonosaurus','Dahalokely','Dakotadon','Dakotaraptor','Damalasaurus','Dandakosaurus','Darwinopterus','Darwinsaurus','Dashanpusaurus','Daspletosaurus','Datanglong','Datousaurus','Dawndraco','Daxiatitan','Deinocheirus','Deinodon','Deinonychus','Delapparentia','Deltadromeus','Demandasaurus','Dendrorhynchoides','Dermodactylus','Diabloceratops','Diamantinasaurus','Diclonius','Dicraeosaurus','Dilong','Dilophosaurus','Diluvicursor','Dimorphodon','Dinheirosaurus','Dinodocus','Diopecephalus','Diplodocus','Diplotomodon','Djupedalia','Dolichorhynchops','Dolichosuchus','Dollodon','Domeykodactylus','Domeykosaurus','Dongbeititan','Dongyangopelta','Dongyangosaurus','Doratorhynchus','Dorygnathus','Draconyx','Dracopelta','Dracoraptor','Dracorex','Dracovenator','Dravidosaurus','Dreadnoughtus','Drinker','Dromaeosauroides','Dromaeosaurus','Dromiceiomimus','Drusilasaura','Dryosaurus','Dryptosauroides','Dryptosaurus','Dsungaripterus','Dubreuillosaurus','Duriatitan','Duriavenator','Dynamoterror','Dyoplosaurus','Dysalotosaurus','Dysganus','Dyslocosaurus','Dystrophaeus','Echinodon','Edgarosaurus','Edmarka','Edmontonia','Edmontosaurus','Efraasia','Einiosaurus','Ekrixinatosaurus','Elaltitan','Elanodactylus','Elaphrosaurus','Elasmosaurus','Elmisaurus','Elopteryx','Elrhazosaurus','Emausaurus','Enigmosaurus','Eoabelisaurus','Eoazhdarcho','Eobrontosaurus','Eocarcharia','Eocursor','Eodromaeus','Eolambia','Eomamenchisaurus','Eoplesiosaurus','Eopteranodon','Eoraptor','Eosinopteryx','Eosipterus','Eotrachodon','Eotriceratops','Eotyrannus','Eousdryosaurus','Epachthosaurus','Epanterias','Epichirostenotes','Epidendrosaurus','Epidexipteryx','Equijubus','Erectopus','Eretmosaurus','Erketu','Erliansaurus','Erlikosaurus','Eromangasaurus','Eshanosaurus','Eucamerotus','Eucercosaurus','Eucnemesaurus','Eudimorphodon','Eugongbusaurus','Euhelopus','Euoplocephalus','Eurazhdarcho','Euronychodon','Europasaurus','Europatitan','Europejara','Europelta','Eurycleidus','Euskelosaurus','Eustreptospondylus','Fabrosaurus','Falcarius','Faxinalipterus','Feilongus','Fenghuangopterus','Ferganasaurus','Ferganocephale','Fostoria','Fresnosaurus','Fruitadens','Fukuiraptor','Fukuisaurus','Fukuititan','Fukuivenator','Fulengia','Fulgurotherium','Fusuisaurus','Futabasaurus','Futalognkosaurus','Gadolosaurus','Galeamopus','Gallardosaurus','Galleonosaurus','Gallimimus','Gallodactylus','Galvesaurus','Gannansaurus','Ganzhousaurus','Gargoyleosaurus','Garudimimus','Gasosaurus','Gasparinisaura','Gastonia','Gegepterus','Geminiraptor','Genusaurus','Genyodectes','Georgiasaurus','Geosternbergia','Geranosaurus','Germanodactylus','Gideonmantellia','Giganotosaurus','Gigantoraptor','Gigantspinosaurus','Gilmoreosaurus','Giraffatitan','Glacialisaurus','Gladocephaloideus','Glishades','Glyptodontopelta','Gnathosaurus','Gobiceratops','Gobiraptor','Gobisaurus','Gobititan','Gobivenator','Gojirasaurus','Gondwanatitan','Gongbusaurus','Gongpoquansaurus','Gongxianosaurus','Gorgosaurus','Goyocephale','Graciliceratops','Graciliraptor','Grallator','Gravitholus','Gronausaurus','Gryphoceratops','Gryposaurus','Guaibasaurus','Gualicho','Guanlong','Guidraco','Gwawinapterus','Gyposaurus','Hadrosaurus','Hagryphus','Halticosaurus','Hamipterus','Hanssuesia','Hanwulosaurus','Haopterus','Haplocanthosaurus','Haplocheirus','Harpactognathus','Harpymimus','Hastanectes','Hatzegopteryx','Hauffiosaurus','Haya','Heilongjiangosaurus','Heishansaurus','Helioceratops','Heptasteornis','Herbstosaurus','Herrerasaurus','Hesperonychus','Hesperosaurus','Heterodontosaurus','Hexing','Hexinlusaurus','Heyuannia','Hippodraco','Histriasaurus','Homalocephale','Hongshanopterus','Hongshanosaurus','Hoplitosaurus','Horshamosaurus','Huabeisaurus','Huanghetitan','Huanhepterus','Huaxiagnathus','Huaxiaosaurus','Huaxiapterus','Huayangosaurus','Hudiesaurus','Huehuecanauhtlus','Hulsanpes','Hungarosaurus','Hydrorion','Hydrotherosaurus','Hylaeosaurus','Hypacrosaurus','Hypselosaurus','Hypselospinus','Hypsibema','Hypsilophodon','Iberomesornis','Ichthyovenator','Ignavusaurus','Iguanacolossus','Iguanodon','Ikrandraco','Iliosuchus','Ilokelesia','Imperobator','Incisivosaurus','Indosaurus','Indosuchus','Ingridia','Inosaurus','Irritator','Isaberrysaura','Isanosaurus','Ischyrosaurus','Isisaurus','Istiodactylus','Itemirus','Iuticosaurus','Jainosaurus','Jaklapallisaurus','Janenschia','Jaxartosaurus','Jeholopterus','Jeholosaurus','Jeyawati','Jianchangnathus','Jianchangopterus','Jianchangosaurus','Jiangjunosaurus','Jiangshanosaurus','Jiangxisaurus','Jidapterus','Jinfengopteryx','Jingshanosaurus','Jintasaurus','Jinzhousaurus','Jiutaisaurus','Jobaria','Jubbulpuria','Judiceratops','Juratyrant','Juravenator','Kaatedocus','Kaijiangosaurus','Kaiwhekea','Kakuru','Kangnasaurus','Karongasaurus','Katepensaurus','Kayentavenator','Kazaklambia','Kelmayisaurus','Kemkemia','Kentrosaurus','Kepodactylus','Kerberosaurus','Khaan','Khetranisaurus','Kileskus','Kimmerosaurus','Kinnareemimus','Klamelisaurus','Kol','Koparion','Koreaceratops','Koreanosaurus','Koshisaurus','Kosmoceratops','Kotasaurus','Kritosaurus','Kronosaurus','Kryptodrakon','Kryptops','Kukufeldia','Kulceratops','Kulindadromeus','Kunbarrasaurus','Kundurosaurus','Kunmingosaurus','Kunpengopterus','Labocania','Lacusovagus','Laevisuchus','Lamaceratops','Lambeosaurus','Lametasaurus','Lamplughsaura','Lanasaurus','Lancanjiangosaurus','Lanzhousaurus','Laosaurus','Lapampasaurus','Laplatasaurus','Lapparentosaurus','Laquintasaura','Latenivenatrix','Latirhinus','Leaellynasaura','Leinkupal','Leonerasaurus','Leptoceratops','Leptocleidus','Leptorhynchos','Leshansaurus','Lesothosaurus','Lessemsaurus','Levnesovia','Lexovisaurus','Leyesaurus','Liaoceratops','Liaoningopterus','Liaoningosaurus','Liassaurus','Libonectes','Ligabueino','Ligabuesaurus','Liliensternus','Limaysaurus','Limusaurus','Lingwulong','Linhenykus','Linheraptor','Linhevenator','Liopleurodon','Lirainosaurus','Liubangosaurus','Lonchodectes','Lonchognathosaurus','Loncosaurus','Longchengpterus','Lophorhothon','Lophostropheus','Loricatosaurus','Losillasaurus','Lourinhanosaurus','Lourinhasaurus','Luanchuanraptor','Ludodactylus','Lufengosaurus','Lukousaurus','Luoyanggia','Lurdusaurus','Lusitanosaurus','Lusotitan','Lycorhinus','Lythronax','Maaradactylus','Machairasaurus','Macrogryphosaurus','Macroplata','Macrurosaurus','Magnamanus','Magnapaulia','Magnirostris','Magnosaurus','Magulodon','Magyarosaurus','Mahakala','Maiasaura','Majungasaurus','Malarguesaurus','Malawisaurus','Maleevus','Mamenchisaurus','Mandschurosaurus','Manidens','Mantellisaurus','Mantellodon','Mapusaurus','Maresaurus','Marisaurus','Marshosaurus','Martharaptor','Masiakasaurus','Massospondylus','Matheronodon','Mauisaurus','Maxakalisaurus','Medusaceratops','Megacervixosaurus','Megalneusaurus','Megalosaurus','Megapnosaurus','Megaraptor','Mei','Melanorosaurus','Mendozasaurus','Mercuriceratops','Merosaurus','Mesadactylus','Metriacanthosaurus','Meyerasaurus','Microcephale','Microceratus','Microcleidus','Microcoelus','Microhadrosaurus','Micropachycephalosaurus','Microraptor','Microtuban','Microvenator','Minmi','Minotaurasaurus','Miragaia','Mirischia','Moabosaurus','Mochlodon','Moganopterus','Mojoceratops','Mongolosaurus','Monkonosaurus','Monoclonius','Monolophosaurus','Mononykus','Montanazhdarcho','Montanoceratops','Morelladon','Morenosaurus','Morinosaurus','Moros','Morrosaurus','Morturneria','Mosaiceratops','Mosasaurus','Muraenosaurus','Mussaurus','Muttaburrasaurus','Muyelensaurus','Muzquizopteryx','Mymoorapelta','Mythunga','Naashoibitosaurus','Nambalia','Nankangia','Nanningosaurus','Nanosaurus','Nanotyrannus','Nanshiungosaurus','Nanuqsaurus','Nanyangosaurus','Narambuenatitan','Nasutoceratops','Navajodactylus','Nebulasaurus','Nedcolbertia','Nedoceratops','Neimongosaurus','Nemegtomaia','Nemegtosaurus','Nemicolopterus','Neosodon','Neovenator','Nesodactylus','Neuquenraptor','Neuquensaurus','Newtonsaurus','Ngexisaurus','Nichollsia','Nichollssaura','Nigersaurus','Ningchengopterus','Ningyuansaurus','Niobrarasaurus','Nipponosaurus','Noasaurus','Nodocephalosaurus','Nodosaurus','Nomingia','Nopcsaspondylus','Noripterus','Normanniasaurus','Normannognathus','Nothronychus','Notoceratops','Notocolossus','Notohypsilophodon','Nqwebasaurus','Nurhachius','Nurosaurus','Nuthetes','Nyasasaurus','Nyctosaurus','Occitanosaurus','Ohmdenosaurus','Ojoceratops','Ojoraptorsaurus','Olorotitan','Omeisaurus','Oohkotokia','Opisthocoelicaudia','Oplosaurus','Orcomimus','Orkoraptor','Ornithocheirus','Ornithodesmus','Ornitholestes','Ornithomimoides','Ornithomimus','Ornithopsis','Ornithostoma','Orodromeus','Orthogoniosaurus','Orthomerus','Oryctodromeus','Oshanosaurus','Osmakasaurus','Ostafrikasaurus','Othnielia','Othnielosaurus','Otogosaurus','Ouranosaurus','Overosaurus','Oviraptor','Owenodon','Oxalaia','Ozraptor','Pachycephalosaurus','Pachyrhinosaurus','Pachysuchus','Pakisaurus','Palaeopteryx','Palaeoscincus','Paludititan','Paluxysaurus','Pampadromaeus','Pamparaptor','Panamericansaurus','Panoplosaurus','Panphagia','Pantydraco','Paralititan','Paranthodon','Parapsicephalus','Pararhabdodon','Parasaurolophus','Parksosaurus','Paronychodon','Parvicursor','Patagonykus','Patagosaurus','Pawpawsaurus','Pectinodon','Pedopenna','Pegomastax','Peishansaurus','Pelecanimimus','Pellegrinisaurus','Peloneustes','Peloroplites','Pelorosaurus','Penelopognathus','Pentaceratops','Peteinosaurus','Petrobrasaurus','Phaedrolosaurus','Philovenator','Phobetor','Phosphatodraco','Phuwiangosaurus','Phyllodon','Piatnitzkysaurus','Picrocleidus','Pinacosaurus','Pisanosaurus','Pitekunsaurus','Piveteausaurus','Planicoxa','Plataleorhynchus','Plateosauravus','Plateosaurus','Platyceratops','Plesiohadros','Plesiopleurodon','Plesiopterys','Plesiosaurus','Pleurocoelus','Pliosaurus','Pneumatoraptor','Podokesaurus','Poekilopleuron','Polacanthus','Polycotylus','Polyonax','Polyptychodon','Pradhania','Prejanopterus','Prenocephale','Prenoceratops','Preondactylus','Priconodon','Priodontognathus','Proa','Probactrosaurus','Proceratosaurus','Procompsognathus','Prodeinodon','Propanoplosaurus','Proplanicoxa','Prosaurolophus','Protarchaeopteryx','Protoavis','Protoceratops','Protognathosaurus','Protohadros','Psittacosaurus','Ptenodracon','Pteranodon','Pterodactyl','Pterodactylus','Pterodaustro','Pterofiltrus','Pteromimus','Pteropelyx','Pterorhynchus','Pterospondylus','Puertasaurus','Pukyongosaurus','Pycnonemosaurus','Pyroraptor','Qantassaurus','Qianzhousaurus','Qiaowanlong','Qinglongopterus','Qingxiusaurus','Qinlingosaurus','Qiupalong','Quaesitosaurus','Quetecsaurus','Quetzalcoatlus','Quilmesaurus','Rachitrema','Raeticodactylus','Rahiolisaurus','Rahonavis','Rajasaurus','Rapator','Rapetosaurus','Raptorex','Ratchasimasaurus','Rayososaurus','Rebbachisaurus','Regnosaurus','Rhabdodon','Rhamphinion','Rhamphorhynchus','Rhoetosaurus','Rhomaleosaurus','Richardoestesia','Rinchenia','Rinconsaurus','Riojasaurus','Rocasaurus','Rubeosaurus','Ruehleia','Rugops','Rukwatitan','Rutellum','Ruyangosaurus','Sahaliyania','Saichania','Saltasaurus','Saltriosaurus','Saltriovenator','Sanchusaurus','Sangonghesaurus','Sanjuansaurus','Sanpasaurus','Santanadactylus','Santanaraptor','Sarahsaurus','Sarcolestes','Sarcosaurus','Sarmientosaurus','Saturnalia','Saurolophus','Sauroniops','Sauropelta','Saurophaganax','Sauroplites','Sauroposeidon','Saurornithoides','Saurornitholestes','Savannasaurus','Scansoriopteryx','Scaphognathus','Scelidosaurus','Scipionyx','Sciurumimus','Scolosaurus','Scutellosaurus','Secernosaurus','Seeleyosaurus','Segisaurus','Segnosaurus','Seitaad','Sellacoxa','Sellosaurus','Serendipaceratops','Sericipterus','Shamosaurus','Shanag','Shantungosaurus','Shanweiniao','Shanxia','Shanyangosaurus','Shaochilong','Shenzhoupterus','Shenzhousaurus','Shidaisaurus','Shixinggia','Shuangmiaosaurus','Shunosaurus','Shuvuuia','Siamodon','Siamosaurus','Siamotyrannus','Siats','Sigilmassasaurus','Siluosaurus','Silvisaurus','Similicaudipteryx','Simolestes','Sinocalliopteryx','Sinoceratops','Sinocoelurus','Sinopliosaurus','Sinopterus','Sinornithoides','Sinornithomimus','Sinornithosaurus','Sinosauropteryx','Sinosaurus','Sinotyrannus','Sinovenator','Sinraptor','Sinusonasus','Siroccopteryx','Skorpiovenator','Sonidosaurus','Sonorasaurus','Sordes','Soriatitan','Sphaerotholus','Spinophorosaurus','Spinops','Spinosaurus','Spinostropheus','Spondylosoma','Staurikosaurus','Stegoceras','Stegopelta','Stegosaurides','Stegosaurus','Stenonychosaurus','Stenopelix','Stephanosaurus','Stokesosaurus','Stratesaurus','Streptospondylus','Stretosaurus','Struthiomimus','Struthiosaurus','Stygimoloch','Styracosaurus','Styxosaurus','Suchomimus','Suchosaurus','Sugiyamasaurus','Sulaimanisaurus','Supersaurus','Suskityrannus','Suuwassea','Suzhousaurus','Szechuanosaurus','Talarurus','Talenkauen','Talos','Tambatitanis','Tangvayosaurus','Tanius','Tanycolagreus','Tanystrosuchus','Taohelong','Tapejara','Tapuiasaurus','Tarascosaurus','Tarbosaurus','Tarchia','Tastavinsaurus','Tatankacephalus','Tatankaceratops','Tataouinea','Tatenectes','Tatisaurus','Taurovenator','Taveirosaurus','Tawa','Tazoudasaurus','Tehuelchesaurus','Teinurosaurus','Telmatosaurus','Tendaguria','Tenontosaurus','Teratophoneus','Terminonatator','Tethyshadros','Texacephale','Texasetes','Teyuwasu','Thalassiodracon','Thalassodromeus','Thalassomedon','Thanos','Thaumatosaurus','Thecocoelurus','Thecodontosaurus','Thecospondylus','Theiophytalia','Therizinosaurus','Thescelosaurus','Thespesius','Thililua','Thotobolosaurus','Tianchisaurus','Tianyulong','Tianyuraptor','Tianzhenosaurus','Tichosteus','Tienshanosaurus','Timimus','Titanoceratops','Titanosaurus','Tochisaurus','Tonganosaurus','Tonouchisaurus','Tornieria','Torosaurus','Torvosaurus','Trachodon','Traukutitan','Triceratops','Trigonosaurus','Trimucrodon','Trinacromerum','Trinisaura','Troodon','Tropeognathus','Tsaagan','Tsagantegia','Tsintaosaurus','Tuarangisaurus','Tugulusaurus','Tuojiangosaurus','Tupandactylus','Tupuxuara','Turanoceratops','Turiasaurus','Tylocephale','Tyrannosaurus','Tyrannotitan','Uberabatitan','Udanoceratops','Ultrasaurus','Umoonasaurus','Unaysaurus','Unenlagia','Unescoceratops','Unquillosaurus','Urbacodon','Utahceratops','Utahraptor','Uteodon','Vagaceratops','Vahiny','Valdoraptor','Valdosaurus','Variraptor','Vectidraco','Vectocleidus','Velafrons','Velocipes','Velociraptor','Velocisaurus','Venenosaurus','Veterupristisaurus','Vinialesaurus','Vitakridrinda','Vitakrisaurus','Volgadraco','Volkheimeria','Vouivria','Vulcanodon','Wakinosaurus','Walgettosuchus','Wannanosaurus','Weewarrasaurus','Wellnhoferia','Wenupteryx','Westphaliasaurus','Willinakaqe','Wintonotitan','Woolungasaurus','Wuerhosaurus','Wukongopterus','Wulagasaurus','Wulatelong','Xenoceratops','Xenoposeidon','Xenotarsosaurus','Xianshanosaurus','Xiaosaurus','Xiaotingia','Xinjiangovenator','Xinjiangtitan','Xiongguanlong','Xixianykus','Xixiasaurus','Xixiposaurus','Xuanhanosaurus','Xuanhuaceratops','Xuwulong','Yamaceratops','Yandusaurus','Yangchuanosaurus','Yaverlandia','Yibinosaurus','Yimenosaurus','Yingshanosaurus','Yinlong','Yixianopterus','Yixianosaurus','Yizhousaurus','Yongjinglong','Yuanmousaurus','Yueosaurus','Yulong','Yunganglong','Yunnanosaurus','Yunxianosaurus','Yurgovuchia','Yutyrannus','Yuzhoupliosaurus','Zalmoxes','Zanabazar','Zapalasaurus','Zapsalis','Zarafasaura','Zby','Zephyrosaurus','Zhanghenglong','Zhejiangopterus','Zhejiangosaurus','Zhenyuanopterus','Zhongornis','Zhongyuansaurus','Zhuchengceratops','Zhuchengtyrannus','Ziapelta','Zigongosaurus','Zizhongosaurus','Zuniceratops','Zuolong','Zupaysaurus','Zuul']
        dino_names_ls = []
        for dino_name in dino_names_org:
            dino_names_ls.append(dino_name.lower())
        return dino_names_ls

    def validate_dino_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(tracker.latest_message)
        #print(tracker.events[-3:])

        lower_dino_names = self.dino_names_db()

        if slot_value.lower() in lower_dino_names:
            return {"dino_name": slot_value.capitalize()}
        else:
            dispatcher.utter_message(response = "utter_wrong_dino_name")
            test_name = slot_value.lower()
            match_dino_ls = ""
            match_ratio_ls = process.extractBests(test_name, lower_dino_names, limit=3, score_cutoff=75)
            #print(match_ratio_ls)
            if len(match_ratio_ls) >0:
                buttons = []
                for dino in match_ratio_ls:
                    #match_dino_ls = "-" + match_dino_ls + dino[0].capitalize() + "\n"
                    payload = "/inform{\"dino_name\": \""+ dino[0].capitalize()+"\"}"
                    buttons.append({"title":"{}".format(dino[0].capitalize()), "payload": payload})
                buttons.append({"title":"None", "payload": "/not_match"})
            #dispatcher.utter_message(text = match_dino_ls)
                dispatcher.utter_message(text = "But I found some similar names. Do you mean ..." , buttons= buttons)
            else:
                dispatcher.utter_message(response="utter_check_dino_name")
            return {"dino_name": None}
#
class AskForDinoNameAction(Action):
    def name(self) -> Text:
        return "action_ask_dino_form_dino_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict,
        ) -> List[EventType]:
        try:
            template = tracker.events[-3]["metadata"]["utter_action"]
        except:
            template = None
        print(template)
        if template != "utter_wrong_dino_name":
            dispatcher.utter_message(response="utter_ask_dino_form_dino_name")
        #else:
        #    dispatcher.utter_message(response="utter_check_dino_name")
        return []

class ActionBriefDino(Action):
    def name(self) -> Text:
        return "action_brief_dino"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dino_name = tracker.get_slot("dino_name")
        URL = "https://dinosaurpictures.org/" + dino_name.capitalize() + "-pictures"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        text = "Quick facts about "
        facts_list = soup.find_all(lambda tag: tag.name == "p" and text in tag.text)
        response_text = "Here is the brief info of " + dino_name.capitalize() +": \n"
        if len(facts_list) > 0:
            for fact in facts_list:
                for f in fact.find_all("li"):
                    response_text = response_text + "- " + f.text +"\n"
        else:
            text = dino_name.capitalize() + " was a "
            short_descr = soup.find(lambda tag: tag.name == "p" and text in tag.text)
            response_text = response_text + short_descr.text
        img_link = soup.find("img", {'title': dino_name})
        dispatcher.utter_message(text=response_text)
        try:
            img_src = img_link['data-src']
        except:
            img_src = img_link['src']
        dispatcher.utter_message(image = img_src)
        return [AllSlotsReset()]
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
