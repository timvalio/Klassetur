# -*- coding: utf-8 -*-
"""Bilder, koordinater, beskrivelser og fasiliteter.

Hotellbilder, beskrivelser og fasiliteter er hentet fra booking.com 14.11.2026.
Aktivitetsbilder er fra Wikimedia Commons med fotograf og lisens oppgitt.
Koordinater er slått opp i Nominatim; omtrentlig=True betyr at bare stedet
er funnet, ikke selve bygningen.
"""

BASIS = [41.63573, 2.70659]

HOTELL = {
 "safari": {
  "koord": [
   41.61329,
   2.65761
  ],
  "omtrentlig": True,
  "beskrivelse": "Situated just 350 metres from Calella Beach, Aparthotel Safari offers an outdoor pool and sun terrace. Free Wi-Fi and satellite TV are included in each functional apartment and studio.",
  "fasiliteter": [
   "Terrasse",
   "Nattklubb/DJ",
   "Sykkelutleie",
   "Utendørsbasseng",
   "Bar",
   "Solsenger eller strandstoler",
   "Turistinformasjon",
   "Restaurant"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/95926390.jpg?k=8d5e9dbb30282e49ad56a9691871a43621842c305de1094808c5c17076b75d79",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/95923425.jpg?k=40b2e2ac4d3b6cefe80bffd4d37c7b13e84ce046fa78ab8d5805a558f23b78c6",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/95922941.jpg?k=b376a35035b258b65d53f6820c885fe67e8548f8cf0664d1de4f4e1d03117115",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/30931850.jpg?k=a98b6c98ad73ade4ddade18d01e98506f25c2dbe976b8aa71df09e5cae33c918"
  ]
 },
 "odissea-park": {
  "koord": [
   41.63409,
   2.72093
  ],
  "omtrentlig": False,
  "beskrivelse": "I Santa Susanna ligger Aparthotel Odissea Park, som tilbyr overnatting med terrasse eller balkong i tillegg til gratis WiFi, TV (flatskjerm) samt et utendørsbasseng og en fellesstue. Privat parkering finnes på overnattingsstedet.",
  "fasiliteter": [
   "Terrasse",
   "Privat parkering",
   "Utendørsbasseng",
   "Bar",
   "Strand",
   "Turistinformasjon",
   "Handikapvennlig",
   "Klesvask"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/647638000.jpg?k=d7cc7129948aa5bf36af62985cf3fae7a6b0e105909575df6a05607fdc69c25b",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/139897882.jpg?k=aad69913b1d1ea40e08793bc27418d63d28254e785068ab9978aba9eed0d6da8",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/647637956.jpg?k=bb15c449a52958e4529922ea8a9df18526a3f0d2e4694249b72c5e3aec116c32",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/106148553.jpg?k=5baa52325e530ed99dda76274ed93802f2946662ceee36f4caf1b2d774b6cdb6"
  ]
 },
 "sant-jordi-santa-susanna": {
  "koord": [
   41.63618,
   2.72495
  ],
  "omtrentlig": False,
  "beskrivelse": "Located 150 metres from the beach on the Costa Maresme, htop Summer Sun is located a few metres from the centre of Santa Susana. It offers an outdoor pool and rooms with balcony.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "2 bassenger",
   "Bar",
   "Beliggenhet ved stranden",
   "Turistinformasjon",
   "Røykfrie rom",
   "Restaurant"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/569657223.jpg?k=4930f362178b865486ed706afa27968d9008f0e5a75bab7e91b4b8c223d5ea49",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/199860461.jpg?k=2614a12e5634cbb653c15f10db11e4e21680cc3acea464cfeeabf8fad296a012",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/132027526.jpg?k=9bce50f886c864e64423d6dfb484335802c64248dda7610593e60a662aac7d6e",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/170844983.jpg?k=feea7fff659acd97cb3f36993614930f882ba6f37c69fb697046fa21a4665a6f"
  ]
 },
 "santa-susanna-chic-apartments": {
  "koord": [
   41.6385,
   2.7075
  ],
  "omtrentlig": False,
  "beskrivelse": "SANTA SUSANNA Chic! Apartments by ALEGRIA ligger i Santa Susanna, 13 km fra Lloret de Mar og 39 km fra Girona, og tilbyr utendørsbasseng og gratis WiFi. Privat parkering er tilgjengelig på stedet.",
  "fasiliteter": [
   "Terrasse",
   "Privat parkering",
   "Utendørsbasseng",
   "Solsenger eller strandstoler",
   "Hage",
   "Klesvask",
   "Røykfrie rom",
   "Familierom"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/495520045.jpg?k=d5ccb453648aa8d377edf9259bbfd21de521af9e647a35c1044549013ca74754",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/495520122.jpg?k=a1991df4e583ec5b4b8601940fe1de0499ded6464fd8bf17609284fe04aac0af",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/495520060.jpg?k=d303eb834df3a63b2ce32d8a70f905284b03a20ebbce45385c9643fde5074fb7",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/495520128.jpg?k=4c1b2da9f03fd60232cf58b99e35285074faa99e2e308dd351ee78b42d914049"
  ]
 },
 "htopplanamar": {
  "koord": [
   41.64018,
   2.73663
  ],
  "omtrentlig": False,
  "beskrivelse": "Set just 50 metres off a beautiful sandy beach, this holiday hotel is the perfect place for a fun family holiday on Catalonia's Costa Maresme, in the resort of Malgrat de Mar.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Utendørsbasseng",
   "Bar",
   "Beliggenhet ved stranden",
   "Hage",
   "Turistinformasjon",
   "Røykfrie rom"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/198922043.jpg?k=04cd1b205ef43e4ace084e26fc9a66b44f06fa813d540e668b7dac38e7714fe6",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/198922110.jpg?k=f32a23e68a23a0b06a5492cc6c840ebd995e6dbfb206127d3317a77061957f8b",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/198922011.jpg?k=3f0960368335a691af0538b4eeedd061139273f96523b51d78a27b453a8f470b",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/198921853.jpg?k=d2c2ebba48095b60d002fe065c206fbb3a253771592cfcdb7d3354c8b05ec3a7"
  ]
 },
 "haromar": {
  "koord": [
   41.61065,
   2.65156
  ],
  "omtrentlig": False,
  "beskrivelse": "Dette familiedrevne hotellet ligger langs strandpromenaden, rett overfor stranden i Calella. Gratis Wi-Fi tilbys i fellesområdene. Rommene har aircondition, flisgulv og egen balkong.",
  "fasiliteter": [
   "Terrasse",
   "Privat parkering",
   "Utendørsbasseng",
   "Bar",
   "Beliggenhet ved stranden",
   "Turistinformasjon",
   "Restaurant",
   "Familierom"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/708076744.jpg?k=a27e9226469c44ed93018589a51f6d27092da903a33af6c5fcb3ca02ee516702",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/708822644.jpg?k=036d2cd8227d81cc6ca19a290c56f79dcedae782f4cc980000e048caa29873cb",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/376035917.jpg?k=6792ef144cb0487ce0cde41ea8785ed24ea5c301a79f36e8da4ca1a326f3287e",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/18160498.jpg?k=cf7608df6f0b5a9c84864de61ecc31d234df205b196112492502e15b00cd39da"
  ]
 },
 "president-calella": {
  "koord": [
   41.6147,
   2.65113
  ],
  "omtrentlig": False,
  "beskrivelse": "Hotel President ligger på Maresmekysten i Catalonia, 500 meter fra Calellastranden og sentrum. Hotellet byr på 3 utendørsbassenger i en hage på 2000 m².",
  "fasiliteter": [
   "Terrasse",
   "Utendørsbasseng",
   "Bar",
   "Hage",
   "Turistinformasjon",
   "Restaurant",
   "Familierom",
   "Døgnåpen resepsjon"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/151247802.jpg?k=e71b0d2cbc39ff4bc50149fb200337ee02c98f906d4af047f9b9c73cd9242615",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/891277709.jpg?k=dcb466df2a558bd4288c1edf363d2fc0d67ec3237f2300cde29d569586ee7005",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/46549873.jpg?k=28dd7e8e3963e400b26842b58b285eee58d5a331ecf71ed8b470665f158b0c48",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/891277147.jpg?k=bcd390a0d9f5c581de1bf541fc80b65683adf558c875df48d30d56bd51a48dbe"
  ]
 },
 "boutique-rivolto-rooms": {
  "koord": [
   41.6375,
   2.711
  ],
  "omtrentlig": False,
  "beskrivelse": "Hostal Boutique - Rivolto Rooms ligger i Santa Susanna og har en terrasse, restaurant, bar og gratis WiFi over hele overnattingsstedet. Water World badeland ligger 15 kilometer unna.",
  "fasiliteter": [
   "Terrasse",
   "Avgiftsfri parkering",
   "Bar",
   "Røykfrie rom",
   "Restaurant",
   "Familierom",
   "Klimaanlegg",
   "Gratis Wi-Fi"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/768676468.jpg?k=3a5e349f2ab21ec229a5f52245229078b97484a9d58d353e5f727287eff5a0c2",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/769744535.jpg?k=272731ab3925387f5a9e4ea114968902a405f8e8571364117d57f21965f2c854",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/769635995.jpg?k=a0bf8eff56ab2f288a7ba9545f0c5ffea1974207b81b327451be3880d19d1b6c",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/769744552.jpg?k=a9dcc7ecd2fded7dd779f4f6cab880481ae6e925786c60e8cff0e434c95eefcd"
  ]
 },
 "internacional": {
  "koord": [
   41.61329,
   2.65761
  ],
  "omtrentlig": True,
  "beskrivelse": "Hotel Internacional is just 50 metres from the beach in Calella, 50 km from Barcelona and Girona. It offers a seasonal outdoor pool and rooms with a private balcony.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Sykkelutleie",
   "Privat parkering",
   "Utendørsbasseng",
   "Bar",
   "Beliggenhet ved stranden",
   "Turistinformasjon"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/371321984.jpg?k=9070617a1c693af67a827bf2fc96009d067de50473f4223b1f55cf2f963f47c2",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/834978685.jpg?k=b1e588b37d48fdcde75e4f11a608988fef1ee7dfe57b423b5f2e3dacd94fa18a",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/834978708.jpg?k=0681b133ec9698a0044b1244fcdf613e2fc8b51586db69b0dcd12619a1fbc2bf",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/371693027.jpg?k=24c78a35b7fa69813b33f7e9fb2941d10ed602423edc8069905cc71abc703d2b"
  ]
 },
 "alhambra": {
  "koord": [
   41.63563,
   2.72433
  ],
  "omtrentlig": False,
  "beskrivelse": "Just 100 metres from the beach in Santa Susanna, the Hotel Alhambra has a large swimming pool and a range of entertainment for children and adults.",
  "fasiliteter": [
   "Terrasse",
   "Nattklubb/DJ",
   "3 bassenger",
   "Bar",
   "Solsenger eller strandstoler",
   "Turistinformasjon",
   "Handikapvennlig",
   "Røykfrie rom"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/150814384.jpg?k=53917dc69a3a51aaaeba60c9f036ce5ccb2c81b9e8cf9d0cffdcc56f6b0648e8",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/221763437.jpg?k=8a54704436bdbcefb1aa0bd98f5343d0f6adf9940f45e2359bc9b70050c578fb",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/221754307.jpg?k=b33603f1b580bdad5eed30a6bcab5e47dc715057acf392aa116e668132a4d433",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/51401795.jpg?k=0533f2c59c225e93749c66d5bb6e59515ce378f720092b4a6541b2da4768de49"
  ]
 },
 "reymar-playa": {
  "koord": [
   41.64591,
   2.74141
  ],
  "omtrentlig": True,
  "beskrivelse": "Reymar Playa Hotel ligger ved strandpromenaden i Malgrat de Mar sentrum, og tilbyr innkvartering og et utendørsbasseng. De romslige rommene har klimaanlegg, flatskjerm-TV og balkong.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Avgiftsfri parkering",
   "Utendørsbasseng",
   "Bar",
   "Beliggenhet ved stranden",
   "Turistinformasjon",
   "Handikapvennlig"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/139219712.jpg?k=122419af591303d94255e2b35f893a2ba987a43fcc21a276b572af21c4a5961b",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/297165048.jpg?k=f45422e41c2c15405fdc7c5a9754d90642bd82063c68adbc4e248f26a5c7725e",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/32169169.jpg?k=d782fa77eb3d66caaed9ce304b744b348dc604d8ca9dbc9eb67627fac6f92000",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/139220754.jpg?k=18646773cae8ef99aa1aabef114c59e97e6c4ee0600cf09efeb2815f41cb45d0"
  ]
 },
 "hotel-maritim": {
  "koord": [
   41.61148,
   2.65378
  ],
  "omtrentlig": False,
  "beskrivelse": "Hotel Maritim ligger 5 minutters gange fra Calella sentrum, og har utsikt over stranden Garbí. Hotellet tilbyr takterrasse med boblebad, gratis Wi-Fi og utendørsbasseng.",
  "fasiliteter": [
   "Terrasse",
   "Sykkelmuligheter",
   "Privat parkering",
   "3 bassenger",
   "Bar",
   "Beliggenhet ved stranden",
   "Turistinformasjon",
   "Handikapvennlig"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/458017639.jpg?k=81e639299caeff07d2b4d485b5c3b800f3bb808344e5e023ed75be60bac00829",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/712629403.jpg?k=9e50f49ea31996c9428410ee88d2bd630e28626b4151767599d1dad5e74e5fd6",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/591469099.jpg?k=595e493e6610976cebf1dad63551349acd23d46aae55514a25f0f089bf4fed08",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265527451.jpg?k=e3fedfbfdcb8b88b14717652b29fae69379818c246927c5cf53fd1993ea5df2a"
  ]
 },
 "mar-blau-calella": {
  "koord": [
   41.61419,
   2.65119
  ],
  "omtrentlig": False,
  "beskrivelse": "Hotel Mar Blau ligger på Maresmekysten, 450 meter fra stranden i Calella, og har 2 utendørsbassenger, treningssenter og rom med egen balkong.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Sykkelutleie",
   "Parkeringsplass",
   "2 bassenger",
   "Bar",
   "Solsenger eller strandstoler",
   "Hage"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/57151694.jpg?k=abbac3ba032e8f285f5d57c433caa4642601a48505ab5c0bfb81166b9f4cad44",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/571112061.jpg?k=dd516cc5f03303b3c8c22c62cca0b0a72b43798f79d1b80e9a262e45c5d0daca",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/687518794.jpg?k=7868e418241aac8c8d75bbe3c355a0e664cd81f5be42880ac698c6ffed344097",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/253364591.jpg?k=0141861052bb7a3aa89d3a60e800102c627ded2757b4db8c8c436731e9e8dfb8"
  ]
 },
 "aqua-aquamarina": {
  "koord": [
   41.632,
   2.704
  ],
  "omtrentlig": False,
  "beskrivelse": "AQUA Hotel Aquamarina & Spa ligger rundt et stort utendørsbasseng, 150 meter fra stranda i Santa Susanna. Hotellet har restaurant, sportsanlegg og rom med balkong.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Sykkelutleie",
   "Privat parkering",
   "3 bassenger",
   "Bar",
   "Strand",
   "Hage"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/579953968.jpg?k=b5bcf5f16b684c6a80d32d53affecc492ad71ae38ee82b63f74521d9e59bf655",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/81056265.jpg?k=8792dfa0e2db2e5f7b449a7dff88178b70de6c3b7f4fa2ec77ece6cb5a8de24f",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/21284993.jpg?k=bd62eb0774e2222c396192387aca1b94614799126bccf35c721b90675c623f2a",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/579954152.jpg?k=08f55e6f7052a72ce6fa4f3712503eda3da97215c974a141e26775a91080ab07"
  ]
 },
 "alegria-florida-park": {
  "koord": [
   41.6318,
   2.702
  ],
  "omtrentlig": False,
  "beskrivelse": "Dette hotellet ligger 1 minutts gange fra stranden i Santa Susanna og har spa. Strendene ligger bare 75 meter unna.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Privat parkering",
   "Innendørsbasseng",
   "Bar",
   "Strand",
   "Hage",
   "Turistinformasjon"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/550649613.jpg?k=6b65c7b23f4a6ab3e5ca6027935b8a47bacbb895b766d6ab318a3df1f63f77cd",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/550649713.jpg?k=06d050e5458b9b89bb8e2f3a8b73902e6b63dd8a710c63653146340b62b3829d",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/550651231.jpg?k=ee56c735fac5c038922030cca71d10210f8c41e6ec225a4ecccdf2ab5a573269",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/550651102.jpg?k=e76ad82fb31442befe92868fbb3ce611776f7cf75f0c30e42a4df715d328ab9c"
  ]
 },
 "aqua-onabrava": {
  "koord": [
   41.633,
   2.7065
  ],
  "omtrentlig": False,
  "beskrivelse": "AQUA Hotel Onabrava ligger på strandpromenaden i Santa Susanna. Alle rom har klimaanlegg og møblert balkong, de fleste med utsikt over Middelhavet.",
  "fasiliteter": [
   "Terrasse",
   "Levende musikk/forestillinger",
   "Sykkelutleie",
   "Privat parkering",
   "3 bassenger",
   "Bar",
   "Solsenger eller strandstoler",
   "Hage"
  ],
  "bilder": [
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/862246932.jpg?k=e22d2e7cd00ed2a4d79da3b43df5beab4b3a080c73dbd887fde518024afb21de",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/155213518.jpg?k=e2ffe855ec1470adf94dfdc1b79e6f45a9747fde6c9fcc8389137fd28d666522",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/155213486.jpg?k=7b7d42f2d1999e09808a7e16f1b3eab6687d1e9503847d7f5f20b6267c5fb37f",
   "https://cf.bstatic.com/xdata/images/hotel/max1024x768/291294695.jpg?k=130029d77767bb4d8a5959f26730d3f6b5b8f6888eb384bed2a89684159a0072"
  ]
 }
}

AKT_KOORD = {
 "strand": [
  41.63573,
  2.70659
 ],
 "sagrada": [
  41.4035,
  2.17443
 ],
 "bcn-tog": [
  41.3851,
  2.1734
 ],
 "guell": [
  41.41423,
  2.15246
 ],
 "illafantasia": [
  41.50289,
  2.36371
 ],
 "marineland": [
  41.66113,
  2.75383
 ],
 "waterworld": [
  41.70737,
  2.82762
 ],
 "portaventura": [
  41.08696,
  1.15858
 ],
 "tossa": [
  41.71677,
  2.93403
 ]
}

AKT_BILDER = {
 "strand": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Playa_de_Santa_Susanna_%282%29.JPG/1280px-Playa_de_Santa_Susanna_%282%29.JPG",
   "tittel": "Stranda i Santa Susanna",
   "fotograf": "Alberto-g-rovi",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Playa_de_Santa_Susanna_%283%29.JPG/1280px-Playa_de_Santa_Susanna_%283%29.JPG",
   "tittel": "Stranda i Santa Susanna",
   "fotograf": "Alberto-g-rovi",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Platja_de_les_Dunes%2C_1.jpg/1280px-Platja_de_les_Dunes%2C_1.jpg",
   "tittel": "Platja de les Dunes i Santa Susanna",
   "fotograf": "Isidro Jabato",
   "lisens": "CC BY-SA 4.0"
  }
 ],
 "sagrada": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Simetr%C3%ADa_na_Sagrada_Familia._Barcelona_B30.jpg/1280px-Simetr%C3%ADa_na_Sagrada_Familia._Barcelona_B30.jpg",
   "tittel": "Sagrada Família innvendig",
   "fotograf": "Luis Miguel Bugallo Sánchez",
   "lisens": "CC BY-SA 3.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Sagrada_Familia%2C_Barcelona_%28P1170693%29.jpg/1280px-Sagrada_Familia%2C_Barcelona_%28P1170693%29.jpg",
   "tittel": "Sagrada Família utvendig",
   "fotograf": "Matti Blume",
   "lisens": "CC BY-SA 4.0"
  }
 ],
 "bcn-tog": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Barcelona_-_Passeig_de_Gr%C3%A0cia_-_Casa_Amatller_%26_Casa_Batll%C3%B3.jpg/1280px-Barcelona_-_Passeig_de_Gr%C3%A0cia_-_Casa_Amatller_%26_Casa_Batll%C3%B3.jpg",
   "tittel": "Casa Batlló og Casa Amatller på Passeig de Gràcia",
   "fotograf": "Txllxt TxllxT",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Platja_de_la_Barceloneta_2018.jpg/1280px-Platja_de_la_Barceloneta_2018.jpg",
   "tittel": "Bystranda Barceloneta",
   "fotograf": "Nicholas Gemini",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Barcelona_-_Barri_Gotic._Carrer_dels_Arcs.jpg/1280px-Barcelona_-_Barri_Gotic._Carrer_dels_Arcs.jpg",
   "tittel": "Gotikerkvarteret i Barcelona",
   "fotograf": "Fred Romero",
   "lisens": "CC BY 2.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Estaci%C3%B3_d%27Arenys_de_Mar_05_2018.jpg/1280px-Estaci%C3%B3_d%27Arenys_de_Mar_05_2018.jpg",
   "tittel": "R1-toget, samme linje som går fra Santa Susanna",
   "fotograf": "9pm",
   "lisens": "CC BY-SA 4.0"
  }
 ],
 "guell": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Park_G%C3%BCell_-_cafe_terrace_01.jpg/1280px-Park_G%C3%BCell_-_cafe_terrace_01.jpg",
   "tittel": "Park Güell",
   "fotograf": "Joe Mabel",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Terrace_of_Parc_G%C3%BCell%2C_Barcelona%2C_Spain.jpg/1280px-Terrace_of_Parc_G%C3%BCell%2C_Barcelona%2C_Spain.jpg",
   "tittel": "Terrassen i Park Güell",
   "fotograf": "Julian Lupyan",
   "lisens": "CC0"
  }
 ],
 "illafantasia": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Slides.jpg/1280px-Slides.jpg",
   "tittel": "Sklier i Illa Fantasia",
   "fotograf": "Illa Fantasia",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Laberint_pirata.jpg/1280px-Laberint_pirata.jpg",
   "tittel": "Piratområdet i Illa Fantasia",
   "fotograf": "Illa Fantasia",
   "lisens": "CC0"
  }
 ],
 "marineland": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Delphinarium_Marineland_Catalogne.jpg/1280px-Delphinarium_Marineland_Catalogne.jpg",
   "tittel": "Delfinshowet i Marineland Catalunya",
   "fotograf": "Olivier Duquesne",
   "lisens": "CC BY-SA 2.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Parc_aquatique_marineland_Catalogne.jpg/1280px-Parc_aquatique_marineland_Catalogne.jpg",
   "tittel": "Vannparken på samme billett",
   "fotograf": "Olivier Duquesne",
   "lisens": "CC BY-SA 2.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Toboggan_Marineland_Catalogne.jpg/1280px-Toboggan_Marineland_Catalogne.jpg",
   "tittel": "Sklie i vannparken",
   "fotograf": "Olivier Duquesne",
   "lisens": "CC BY-SA 2.0"
  }
 ],
 "waterworld": [],
 "portaventura": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Shambhala_in_the_top_%2876_meters%29.JPG/1280px-Shambhala_in_the_top_%2876_meters%29.JPG",
   "tittel": "Shambhala på toppen, 76 meter over bakken",
   "fotograf": "Sotti",
   "lisens": "CC0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Dragon_Khan_Big_Vertical_Loop.jpg/1280px-Dragon_Khan_Big_Vertical_Loop.jpg",
   "tittel": "Dragon Khan gjennom den store loopen",
   "fotograf": "Sotti",
   "lisens": "CC0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Shambhala_Splash.JPG/1280px-Shambhala_Splash.JPG",
   "tittel": "Shambhala gjennom vannet",
   "fotograf": "Sotti",
   "lisens": "CC0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Vue_d%27ensemble_de_ferrari_land.jpg/1280px-Vue_d%27ensemble_de_ferrari_land.jpg",
   "tittel": "Ferrari Land, som ligger vegg i vegg",
   "fotograf": "Ahs 34000",
   "lisens": "CC BY-SA 4.0"
  }
 ],
 "tossa": [
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Costa_Brava_-_Tossa_de_Mar_-_La_Vila_Vella_-_Pla%C3%A7a_Pintor_Roig_Soler_-_View_NNW.jpg/1280px-Costa_Brava_-_Tossa_de_Mar_-_La_Vila_Vella_-_Pla%C3%A7a_Pintor_Roig_Soler_-_View_NNW.jpg",
   "tittel": "Vila Vella i Tossa de Mar",
   "fotograf": "Txllxt TxllxT",
   "lisens": "CC BY-SA 4.0"
  },
  {
   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Costa_Brava_-_Tossa_de_Mar_-_La_Vila_Vella_-_Passeig_del_Mar_-_View_ENE_towards_14th_century_Torre_d%27en_Joan%C3%A0s_%26_Portal_%28Passeig_de_la_Vila_Vella%29.jpg/1280px-Costa_Brava_-_Tossa_de_Mar_-_La_Vila_Vella_-_Passeig_del_Mar_-_View_ENE_towards_14th_century_Torre_d%27en_Joan%C3%A0s_%26_Portal_%28Passeig_de_la_Vila_Vella%29.jpg",
   "tittel": "Bymuren i Tossa de Mar",
   "fotograf": "Txllxt TxllxT",
   "lisens": "CC BY-SA 4.0"
  }
 ]
}
