import time
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "@gcapooo9"
DATA_FILE = "prices_cache.json"

# لستة المنتجات (مختصرة لأول 150 منتج)
PRODUCTS = [
    "https://kenzz.com/en/product/222SEJ8QC6NU/3-Piece-Round-Oven-Casserole-Set",
    "https://kenzz.com/en/product/23L8H6C2MMTL/4-In-1-Lava-Transparent-Laptop-Protector-Stickers",
    "https://kenzz.com/en/product/25P5R3MF8DGH/Evolve-TV-43-inch-FHD-LED-Frameless-VLD43NA",
    "https://kenzz.com/en/product/25SB7VR384NG/Akai-Electric-Oven-With-Grill-And-Fan-Black-45-Liters-Ak-45",
    "https://kenzz.com/en/product/26DQKFKPB5TT/Ariston-Electric-Water-Heater%2C-50-Litres%2C-White-PRO-R",
    "https://kenzz.com/en/product/26SZJV96WLAP/Fresh-Sauce-Blender-1.5L-with-2-Mills",
    "https://kenzz.com/en/product/26WS8M84B3B4/Unionaire-Refrigerator-2-Doors-370-Liters-RD380BS",
    "https://kenzz.com/en/product/26Y3AFANT9SS/Fxp-20-Steering-Wheel-Leather-Cover-Multi-Color",
    "https://kenzz.com/en/product/26Y5TSJMK5CV/Lazord-Granite-Plus-Rectangular-Oven-Casserole-Copper-2-Pieces",
    "https://kenzz.com/en/product/27AV9LTYPPR9/Sharp-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-AY-AP12ZHE",
    "https://kenzz.com/en/product/27GTAQMAGWXA/Ceiling-Fan-56-Inches-Black-Brown",
    "https://kenzz.com/en/product/284354YUVCSM/Smile-Wall-Fan-26-Inch-Black",
    "https://kenzz.com/en/product/28PN4M9ZN428/Efs-95Sr-Stand-Fan-18-Inches-Black",
    "https://kenzz.com/en/product/28WJ5S9YZ4Z5/Midea-Mission-Pro-Air-Conditioner-1.5-HP-Cooling-Only-M1SCT-12CRN-Q8",
    "https://kenzz.com/en/product/29VJLAYGHW5E/Remote-Control-For-Arion-Zoom-Screen-Black",
    "https://kenzz.com/en/product/2A3QFYJKW3PT/FAS2018-Stand-Fan-18-Inch-3-Speeds-Black",
    "https://kenzz.com/en/product/2AG5UVJCSZFP/Stain-Resistant-Microwave-Cover-85*35-Cm",
    "https://kenzz.com/en/product/2AK92F6VE84S/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-SFW13H-IP-SEW13H-O",
    "https://kenzz.com/en/product/2B6DUSYBVKSU/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-FUFW12C-IW",
    "https://kenzz.com/en/product/2C4UKSKQVG2E/Fresh-32-inch-Frameless-HD-LED-Smart-TV-Black-32LH423CT",
    "https://kenzz.com/en/product/2CV3MC88GDHP/Bosch-refrigerator-328-liters-silver-BC-KDN43NL2E8",
    "https://kenzz.com/en/product/2ECMU756CC3J/2-Door-Refrigerator-350-Liters-Black-Urn420Lblbams1",
    "https://kenzz.com/en/product/2FQNMCX9FLM9/NBL500-Electric-Blender-500w-Black-White",
    "https://kenzz.com/en/product/2FTMDVF39JYG/Innovative-Vegetable-Chopper",
    "https://kenzz.com/en/product/2FXVUX4W8WTT/Tornado-Split-Air-Conditioner-1.5-Hp-Fast-Cooling-White-Th-C12Bee",
    "https://kenzz.com/en/product/2GB9HDNDMF7D/Beko-Built-in-Gas-Cooker-7800-Watt-4-Burners-Silver-HIAW64225SX",
    "https://kenzz.com/en/product/2GBPPGPLMXK9/Hisense-Split-Air-Conditioner-2.25-Hp-Cold-And-Hot-Hi-E18Invhp",
    "https://kenzz.com/en/product/2GGALGRNKC8Y/Fresh-Upright-Deep-Freezer-6-Drawers-Without-Touch-Control-Handle-Black-FNU-MRT270B",
    "https://kenzz.com/en/product/2JY57VFRL2YS/Toshiba-10.5kg-Full-Automatic-Inverter-Washing-Machine-with-Dryer-Gray-TWD-BM115GF4EG(MK)",
    "https://kenzz.com/en/product/2LCE8WA9TD49/Electric-Blender-with-2-Grinder-1.5L-White",
    "https://kenzz.com/en/product/2MB97BPNW6BC/Sokany-Grinder-Chopper-DOUBLE-LAYER-Stainless-Bowl-3L-4Blade--800W-(SK-7027)-SK-7027",
    "https://kenzz.com/en/product/2N6B9LKEAPLZ/Stand-Fan-With-Remote-Control-And-Temperature-Sensor%2C-Inverter-Tech%2C-18-Inches-85-Watts",
    "https://kenzz.com/en/product/2NBZZ69TV2CE/Leaves-Mascara-10-ml",
    "https://kenzz.com/en/product/2NTGGZAZ7DS7/Sokani-Digital-Air-Fryer-1800-Watt-Black-SK-10007",
    "https://kenzz.com/en/product/2P45ASAU89FF/Fresh-Professional-Control-Cooker-90-x-60-cm-5-Burners-Black",
    "https://kenzz.com/en/product/2PHSN5PRT28B/Two-Way-Movable-TV-Stand-70-Inch-LX-70",
    "https://kenzz.com/en/product/2Q9HXWXS2K4V/Stainless-steel-grinder-and-chopper-4-liters-800-watts-SK-7028",
    "https://kenzz.com/en/product/2QX4UM8AZLHN/LG-Inverter-Split-Air-Conditioner-5-HP%2C-Cooling-%26-Heating-White-S4-W3R43EA",
    "https://kenzz.com/en/product/2RXVRDF2YD3A/360-Degree-Adjustable-Movable-TV-Mount-65-Inch-Z-180",
    "https://kenzz.com/en/product/2SG769UVZ68F/Oven-Thermal-Bags-3-Pieces-%C3%97-5-Medium",
    "https://kenzz.com/en/product/2SSBULRFV9D2/Adjustable-Laptop-Stand-MDK-AL-1",
    "https://kenzz.com/en/product/2T4XJRBMMYQP/Beko-No-Frost-Refrigerator-390-Liters-Silver-Rdne420Kd",
    "https://kenzz.com/en/product/2TCTVLPNTVC7/Glass-screen-protector-for-iPhone-13Pro-Max",
    "https://kenzz.com/en/product/2U89EUNUHTJZ/Braun-Multiquick-5-Hand-Blender-600-Watt-White-And-Gray-Mq-500",
    "https://kenzz.com/en/product/2UWG4U43XCBD/Toshiba-Midea-Automatic-Top-Loading-Washing-Machine-11-kg-Morandi-Gray-AW-UK1100HUPEG(MK)",
    "https://kenzz.com/en/product/2VYG2JPQ8695/Stainless-Steel-Hand-Blender-4-in-1-1000-Watts-SK-758-4N",
    "https://kenzz.com/en/product/2WAV7VNWZGW4/Zanussi-Cooker-90-cm-5-Burners-Silver-ZCG97326XA",
    "https://kenzz.com/en/product/2WN6YM2Y8EM8/Haier-TV-50-inch-Smart-4K-UHD-LED-TV-with-Built-in-Receiver-H50K80EU",
    "https://kenzz.com/en/product/2WVB7Y23KVT7/Philips-Durgen-Air-Fryer-9-Liter-Capacity-Black-NA350",
    "https://kenzz.com/en/product/2X2PUCG6KLV5/Bosch-Gas-Cooker-With-Oven-And-Grill-Series-2-90-Cm-5-Burners-Hgv1F8Y50S",
    "https://kenzz.com/en/product/2X4HT6GS9YXF/Grohe-Smart-TV-50-inch-4K-Android-LED-Frameless-GLD50SAWORV2",
    "https://kenzz.com/en/product/2XMTDTVUNYCX/Lazord-Granite-Pro-Oven-Trays-3-Pieces-Sizes-24%2C-26%2C-28-cm-Purple",
    "https://kenzz.com/en/product/2XR8F6QXNC3P/LG-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-Black-S4-W24K2RME",
    "https://kenzz.com/en/product/2Y9A9FAUKJPZ/Ufw18E2-Wall-Fan-18-Inches-Black-And-Grey",
    "https://kenzz.com/en/product/2Z5F8MGJULYP/Ariston-Electric-Water-Heater%2C-50-Liters-White-RUBIS-PRO-50-V-EG",
    "https://kenzz.com/en/product/2ZJG4LQ7339U/Pressure-Cooker-Set-7L-Stainless-Steel-Silver",
    "https://kenzz.com/en/product/2ZPW3TBUHQRC/Zanussi-Steam-Max-Washing-Machine-7-Kg-Black-Zwf7221Bl7",
    "https://kenzz.com/en/product/2ZR6HRVS2SMC/Pyrex-Bombay-Thermal-Refrigerator-1.25-L-3942",
    "https://kenzz.com/en/product/32DC7TXAA5B8/Aff1800-B-Air-Fryer-5.5-L",
    "https://kenzz.com/en/product/343H6VUED4WE/Cufan-Baby-Doll-Set",
    "https://kenzz.com/en/product/344R38BEWBF9/Top-Loading-Automatic-Washing-Machine-10-Kg-Silver-Wtla1000Sl",
    "https://kenzz.com/en/product/34AE5QMYQQ3K/Carrier-Split-Optimax-Inverter-Air-Conditioner-2.25-Hp%2C-Cooling-%26-Heating-White-53Qhct18Dn-708F",
    "https://kenzz.com/en/product/36NTVA7UWMG6/HP63R-Foldable-Wired-Headset-with-Microphone-1.5m-Red",
    "https://kenzz.com/en/product/3773D45C4L6M/Alaska-Defrost-Refrigerator-289-Liters-Silver",
    "https://kenzz.com/en/product/39CNHAYM4V7D/Mq-9147X-Braun-Multi-Quick-9-Hand-Blender-Set-1200-Watt",
    "https://kenzz.com/en/product/39HQRRH3EUU2/-500004511-Fresh-Rafael-Ceiling-Fan-56-Inch-White",
    "https://kenzz.com/en/product/39QD48TS77WM/Ariston-Electric-Water-Heater-40-Liters-White-RUBIS-PRO-40-V",
    "https://kenzz.com/en/product/3A2UPTDKE589/Keriazi-Super-Steel-Gas-Cooker-5-Burners-Stainless-Steel-90-cm-8900",
    "https://kenzz.com/en/product/3ATZYSXWYURG/Camera-Lens-Screen-Protector-IPhone-14",
    "https://kenzz.com/en/product/3CDXNDG5YUAZ/Tefal-Stand-Fan-16-Inches-Black-Vy5391E2-",
    "https://kenzz.com/en/product/3DSN4EHXZHRE/Hyundai-43-Inch-Smart-LED-TV-L43HYNDA630",
    "https://kenzz.com/en/product/3ELG4FGDZTSV/Kenwood-Blender-with-2-Grinders-1.5L-Capacity-400W-WhiteBBBB-BLP10.COWH",
    "https://kenzz.com/en/product/3GATA94EQXVP/Hoover-Fully-Automatic-Washing-Machine-8-kg-Inverter-Motor-Silver-H3WS38TAMF7R-ELA",
    "https://kenzz.com/en/product/3GDXZV9Q3PYC/Toshiba-Automatic-Washing-Machine-10-kg-Gray-TW-BK115GF4EG(MK)",
    "https://kenzz.com/en/product/3JFAA3ZLYRYM/Kriazi-Horizontal-Deep-Freezer-336-Liters-White-E336",
    "https://kenzz.com/en/product/3JYXVBAC6FAN/Toshiba-No-Frost-Inverter-Refrigerator-450-Liters-Dark-Grey-GR-RT622WE-PMN(06)",
    "https://kenzz.com/en/product/3K9FSDVUYA36/4-Piece-Window-Screen-Repair-Patch-10-cm",
    "https://kenzz.com/en/product/3KGXEPZ3X5SW/Alaska-Vertical-Deep-Freezer-Defrost-3-Drawer-Control-Brown-UP140",
    "https://kenzz.com/en/product/3L98TBVUVMAS/Zanussi-SteelPlus-Gas-Cooker-5-Burners-with-Oven-ZCG922A6XB",
    "https://kenzz.com/en/product/3LDT2F5VGBEL/Screen-protection-made-of-tempered-glass-for-iPhone-13-Pro-Max",
    "https://kenzz.com/en/product/3NLVJXXE2MQN/Haier-Split-Air-Conditioner-1.5-HP-Cooling-Inverter-Plasma-White-HSU-12KCRIA",
    "https://kenzz.com/en/product/3Q3RFZ859QAH/Tornado-Semi-Automatic-Washing-Machine%2C-7-Kg-Black-Tmh-Hs07C-(Wk)",
    "https://kenzz.com/en/product/3QJHMRDXDQ4R/Ariston-Dishwasher-14-Place-Settings-Front-Load-Silver-LFC-3O33-WLTX",
    "https://kenzz.com/en/product/3QU2BS6X9S2K/Mx40-Mobile-Tv-Stand",
    "https://kenzz.com/en/product/3R667SBNRC3F/Fresh-Microwave-36-Liters-Black-Fmw-36Kc-B",
    "https://kenzz.com/en/product/3S5LTV3L4NT9/Suede-Crossbody-Bag-for-Women-with-Strass-Black-Silver-RM-127",
    "https://kenzz.com/en/product/3SBW3KQ8HVB6/SK-005-Electric-Airfryer-8.5-liters-Black",
    "https://kenzz.com/en/product/3TVU4SC6KXBZ/Wooden-Shape-Sorter-Game",
    "https://kenzz.com/en/product/3TVV5C3ZDGAS/Apple-iPhone-16-Plus-256GB-SIM-Black-5G-(Local-Warranty)",
    "https://kenzz.com/en/product/3TZ96Y9FWZ6X/Fresh-Cooling-Split-Air-Conditioner-2.25-HP-White-FUFW18C-IW-AG-FUFW18C-O-X2",
    "https://kenzz.com/en/product/3UJTV2A5KGTW/Fourira-Palm-Polished-Stainless-Bucket-Brown",
    "https://kenzz.com/en/product/3V2YQBQ2VT6K/Kiriazi-Vertical-Deep-Freezer-5-Drawers-Silver-E230N5-3",
    "https://kenzz.com/en/product/3X3SZXMRRJ46/500ml-Insulated-Travel-Mug-with-LED-Touch-Screen-Blue",
    "https://kenzz.com/en/product/3Y4F5FQMKJWD/Fresh-Electric-Water-Heater-Relax-40-Liters",
    "https://kenzz.com/en/product/3Y9ZVHMFFQRK/Fresh-Microwave%2C-42-Liters%2C-1000-Watts%2C-Digital-Display-Black-FMW-42KC-BW",
    "https://kenzz.com/en/product/3Z3Y3AT3LFRB/Dexil-Rtv-Silicone-Adhesive-Grey-85.2G",
    "https://kenzz.com/en/product/3ZRUTVC88MTP/Luxury-White-Erasers-Pack-of-36-AG-1036-W",
    "https://kenzz.com/en/product/423ZM3XTCHX9/Semi-Automatic-Washing-Machine-Top-Load-5-Kg-White-Shatoora",
    "https://kenzz.com/en/product/42EQLTVRDEKZ/IKEA-503.430.05-Glattis-Coasters-with-Holder%2C-Brass-Color",
    "https://kenzz.com/en/product/43XW7BKFWX4Q/Fresh-Jumbo-Gas-Cooker-5-Burners-90x60-cm-Silver-500016272",
    "https://kenzz.com/en/product/44HNUXVFTFLR/White-Point-Automatic-Top-Loading-Washing-Machine-15-kg-Gray-WPTL150DGSM",
    "https://kenzz.com/en/product/44J454J5K432/Ecomatic-Oven-60-cm-Gas-Grill-Black-Crystal",
    "https://kenzz.com/en/product/44N3SYU6UF7Q/Haier-Split-Air-Conditioner-1.5-Hp-Cold-And-Hot-White-Hsu-12Khrocc",
    "https://kenzz.com/en/product/44XKXQSBG5JD/Bz-50-Smart-Microwave-Mounting-Bracket",
    "https://kenzz.com/en/product/46A8VEREDK64/Reusable-silicone-air-fryer-liner-19-cm-Red",
    "https://kenzz.com/en/product/46GQV3RTF5HB/Automatic-Washing-Machine-Front-Loading-6-Kg-Silver-Wpw61015Pds",
    "https://kenzz.com/en/product/47L3XMBY2HFU/Fresh-washing-machine%2C-top-automatic%2C-10-kg%2C-digital-pump%2C-black%2C-FTM10F12BH",
    "https://kenzz.com/en/product/47TMEFVUW32V/Alaska-Horizontal-Deep-Freezer-135L-Silver-Defrost-CH140",
    "https://kenzz.com/en/product/47VQ9BBVTVLQ/Can-Finger-Spinner-Rotate",
    "https://kenzz.com/en/product/4859H3RQATJV/Beko-No-Frost-Deep-Freezer-168-Liters-Black-Rfnm200E20S",
    "https://kenzz.com/en/product/48FXZRUX7HTA/CHP62.700SI-Electric-chopper-1.2-liters-500-watts-silver",
    "https://kenzz.com/en/product/49RJDBJFU4MB/GH-6SN-W-Natural-Gas-Water-Heater-Without-Chimney-Silver-",
    "https://kenzz.com/en/product/49SPK9TYB2GG/HFP90-Air-Fryer-2000W-11L-Black",
    "https://kenzz.com/en/product/49ZXBH6FDV68/Sharp-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-Digital-Plasma-Cluster-White-AY-AP24ZHE",
    "https://kenzz.com/en/product/4BAN9FX77F9A/Fresh-instant-water-heater-9-kW",
    "https://kenzz.com/en/product/4C45T6VLUKC2/Haier-Front-Load-Inverter-Washing-Machine-8-kg-Silver-HW80-B14959S6TU1",
    "https://kenzz.com/en/product/4C89G9XPWA8L/Beko-Built-in-Gas-Cooker-60-cm-4-Burners-Black-HIAW-64225-BX",
    "https://kenzz.com/en/product/4CB4H6JUJ8DE/Defrost-Alaska-Refrigerator-318-L-12-Feet-Black-Ksd",
    "https://kenzz.com/en/product/4CPN5P3WWJQU/DF-1600-Movable-TV-Monitor-Stand-Black",
    "https://kenzz.com/en/product/4DMGPWCURE55/Atlantic-Electric-Water-Heater-30L-1200-Watt-Concept-A-8312810",
    "https://kenzz.com/en/product/4EXR6PR4WWNZ/Refrigerator-Food-Storage-Container-Set-7-Pieces",
    "https://kenzz.com/en/product/4F4NKAC9EA3L/Jb1023-3*1-Blender-And-Grinder-600-Watts-Black",
    "https://kenzz.com/en/product/4FC2Q2L4LKMR/Samsung-No-Frost-Refrigerator-344-Liters-Black-Rb34T672Fb1-Mr",
    "https://kenzz.com/en/product/4H46QKKN38BZ/Set-of-refrigerator-containers-with-bamboo-lid-2-pieces-500-ml",
    "https://kenzz.com/en/product/4HCA2MUMS78Q/Fresh-Semi-Automatic-Washing-Machine-12-Kg-White-500001730",
    "https://kenzz.com/en/product/4KQGBFSK9BNU/Royal-Gas-Perfect-Cast-Digital-Cooker-5-Burners%2C-60-x-90-cm%2C-Stainless-Steel-2010245",
    "https://kenzz.com/en/product/4L3N5JA74ZCH/Wooden-Refrigerator-Magnets-9-Pieces-Shape-12",
    "https://kenzz.com/en/product/4L4LTSNAE99Q/Anti-Vibration%2C-Shockproof%2C-and-Non-Slip-Rubber-Foot-Pads-for-Washing-Machine%2C-Refrigerator%2C-and-Furniture-8-Pieces",
    "https://kenzz.com/en/product/4MHG63TV5CAC/Anti-anxiety-and-stress-cube-game",
    "https://kenzz.com/en/product/4QF9Y92H3M2G/Beko-No-Frost-Refrigerator-406-Liters-Inverter-Black-Rdne455M20Xbidegb",
    "https://kenzz.com/en/product/4RLSGTHHNJ56/Sharp-Microwave-25-Liters-Black-With-Grill-R250Mgr",
    "https://kenzz.com/en/product/4RTQPVCBE7Q4/Tornado-Cooker-Hood-60-Cm-Stainless-Hos-M60Esu-S",
    "https://kenzz.com/en/product/4RX9B6NYBWHP/Electric-Double-Head-Office-Fan-with-360%C2%B0-Rotation-Dual-Speed-Control",
    "https://kenzz.com/en/product/4RYNB6RR8FY4/Braun-Hand-Blender-700-Watt-White-BC-MQ3020",
    "https://kenzz.com/en/product/4S45SFTVA754/Pressurized-water-dispenser-with-leak-proof-nozzle",
    "https://kenzz.com/en/product/4SPU86GW3VZY/Castle-FAS2518RD-18-Blade-Floor-Fan-Remote-Control-Multicolor",
    "https://kenzz.com/en/product/4SWU3ZC3L35N/12V-Dual-Head-Electric-Car-Fan-Black",
    "https://kenzz.com/en/product/4UQWP537D54J/Bg786-Laptop-Bag-15.6-Inches-Black",
    "https://kenzz.com/en/product/4UUJDG5CASD4/Bsl-130-Wall-Mounted-Tv-Stand",
    "https://kenzz.com/en/product/4V7EMTC8KWK3/Multi-purpose-Blender-2.5l-SK-666",
    "https://kenzz.com/en/product/4W9UWH4LL8MF/Mini-Wonder-Chopper-800-Watt-5-L-SK-7015",
    "https://kenzz.com/en/product/4WASZWTVVU4L/Molfix-Shorts-Size-6-48-Diapers",
    "https://kenzz.com/en/product/4WLVAFMJGY4R/Highcast-Gas-Cooker-5-Burners-Silver",
    "https://kenzz.com/en/product/4WU3WNTVYLCE/Skin-Tone-Hydrocolloid-Patches-For-Acne-And-Cold-Sore-Treatment",
    "https://kenzz.com/en/product/4XBS82NWELKA/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-White-AY-XP18YHE",
    "https://kenzz.com/en/product/4XPMVKAJ7EAQ/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-Only-Silver-AH-XP18UHE",
    "https://kenzz.com/en/product/4XVGM283HMQC/Screen-Remote",
    "https://kenzz.com/en/product/4Z3X9K945LCB/Semi-Automatic-Washing-Machine-Top-Load-4-Kg-White-Fws400Nd",
    "https://kenzz.com/en/product/4ZDUHKK32FUT/Manhattan-4K-Hdmi-Splitter-With-2-Ports-Black",
    "https://kenzz.com/en/product/52ZSXYDUAPLV/Beko-No-Frost-Refrigerator-Freezer-367-Liters-Rdne420K02Dxiteg",
    "https://kenzz.com/en/product/53XLGBZT7Z7H/Toshiba-Top-Load-Washing-Machine-8-Kg-Gray-Aw-M801Apeg(Sg)",
    "https://kenzz.com/en/product/543BFVPZGWK7/Ecomatic-90cm-Gas-Oven-with-Fa-%2C-Crystal-Black-105L",
    "https://kenzz.com/en/product/545WSH57WBJK/Sokany-Chopper-800-Watts-4L-Silver-SK-7028",
    "https://kenzz.com/en/product/56925QBPKCF6/Bl1251A-Electric-Blender-500W-White",
    "https://kenzz.com/en/product/56AB22TQGYYN/Ariston-Electric-Water-Heater%2C-Pro-AR-80-Liters-RUBIS-PRO-80-V-EG",
    "https://kenzz.com/en/product/56MTQARFBCX3/Foldable-Aluminum-Laptop-Stand-Silver",
    "https://kenzz.com/en/product/57QR52BPYHGC/AOF100-B5-Digital-Air-Fryer-12L-Black-Silver",
    "https://kenzz.com/en/product/58JYB55ASMGY/Braun-Multimix-Hand-Blender-450-Watt-Hm-1100",
    "https://kenzz.com/en/product/58LWUXV88AA9/Pressure-Cooker-Set-11L-Aluminum-Silver",
    "https://kenzz.com/en/product/595AJX8LZZ33/Beko-Gas-Cooker-90-Cm-5-Sh-Full-Safety-Black-Ggr15115Dxnb",
    "https://kenzz.com/en/product/59H6MYFRB8E7/Black-%26-Decker-air-fryer-6-in-1-7.2-liters-1500-watts-black-and-silver-AF7257-B5",
    "https://kenzz.com/en/product/59JC3DQ8U2JZ/Zanussi-Digital-Built-in-Electric-Oven-with-Grill-60cm-72L-Stainless-Steel-ZOB35602XK",
    "https://kenzz.com/en/product/5A3TUHGVYB2Y/Digital-Led-Shower-%2B-Screen-5-Pieces-Grey",
    "https://kenzz.com/en/product/5BLLLAYG4USM/FR-48ECCO-Electric-Oven-With-Grill-48-L-Black",
    "https://kenzz.com/en/product/5C97CP35K39W/Fresh-Hand-Blender-Black-HB-800N",
    "https://kenzz.com/en/product/5CGPCS9BE8UB/Audio-Splitter-Cable-For-Headphones-And-Microphone-80-Cm",
    "https://kenzz.com/en/product/5CRURB65XCHH/Jack-32-Inch-HD-LED-TV-Black-32JC3110B",
    "https://kenzz.com/en/product/5CYDNTL2H5ZK/Sharp-Sj-48C(St)-No-Frost-Refrigerator-385-Liters-Silver",
    "https://kenzz.com/en/product/5DNAB4L4MAYV/Black-%26-Decker-HX230-B5-Fan-Heater-White",
    "https://kenzz.com/en/product/5DTTEY66XA3G/TDF16-Desk-Fan-16-Inch-Black-Red",
    "https://kenzz.com/en/product/5EJ63TV8WYYX/Nine-Times-Deodorant-Lollipop-50-ml",
    "https://kenzz.com/en/product/5ER4E2U24QVV/Unionaire-No-Frost-Deep-Freezer-5-Drawers-Digital-Black-UF-205LBLBA-DL",
    "https://kenzz.com/en/product/5FAPAZ4EQ552/Bosch-Hand-Blender-with-Chopper-600-Watt-MSM66155",
    "https://kenzz.com/en/product/5G2DKM7N6VYX/White-Whale-Refrigerator-600-Liters-Stainless-Digital-No-Frost-Inverter-Wr-3068Mxss-Wf3068Ss",
    "https://kenzz.com/en/product/5JA2QV8RJTT5/360-privacy-screen-compatible-with-iPhone13-PRO",
    "https://kenzz.com/en/product/5KXXN3MECA3W/Food-Storage-BinsWithDrainer-Basket%2C-Stackable-Refrigerator-Organizer-Canisters-Set-Of-4",
    "https://kenzz.com/en/product/5LP5PZMELG5B/Fresh-Professional-Cooker-90-x-60-cm-5-Burners-Black",
    "https://kenzz.com/en/product/5LTVDY2QV4RQ/Fine-Fluffy-Tissue-Box-500-Tissue-3-Pcs",
    "https://kenzz.com/en/product/5LYJH77TWMES/Fresh-Professional-Style-Gas-Cooker-5-Burners-Silver-500008130",
    "https://kenzz.com/en/product/5M4UTF6QWNAF/Midea-Dishwasher-14-Person-Capacity-Smart-Wi-Fi-Mdwef1433D(Ss)-Wi-Eg"
]

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"خطأ في حفظ الملف: {e}")

stored_data = load_data()

def send(msg):
    u = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"خطأ في إرسال رسالة التليجرام: {e}")

def check_prices():
    global stored_data
    
    total_products_count = len(PRODUCTS)
    if total_products_count == 0:
        print("\n[⚠️] قائمة المنتجات فارغة حالياً!")
        return
        
    print(f"\n[🔄] بدء فحص عدد {total_products_count} منتج بصمت...")
    
    changes_count = 0
    checked_count = 0
    current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    for index, url in enumerate(PRODUCTS, 1):
        try:
            response = requests.get(url, headers=H, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                print(f"[{index}/{total_products_count}] فشل فحص المنتج (كود الاستجابة: {response.status_code})")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            current_price = None
            product_name = None
            
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    data_items = data if isinstance(data, list) else [data]
                    
                    for item in data_items:
                        if isinstance(item, dict) and item.get('@type') == 'Product':
                            product_name = item.get('name')
                            offers = item.get('offers')
                            if isinstance(offers, dict):
                                p = offers.get('price') or offers.get('lowPrice')
                                if p:
                                    current_price = float(p)
                                    break
                            elif isinstance(offers, list) and len(offers) > 0:
                                p = offers[0].get('price')
                                if p:
                                    current_price = float(p)
                                    break
                    if current_price:
                        break
                except:
                    pass
            
            if not product_name:
                h1 = soup.find('h1')
                product_name = h1.get_text().strip() if h1 else "منتج بدون اسم"
            
            if not current_price:
                price_element = (
                    soup.find('span', {'class': 'price'}) or 
                    soup.find('div', {'class': 'price'}) or 
                    soup.find('span', {'class': 'current-price'}) or
                    soup.find('span', class_=lambda x: x and 'price' in x.lower())
                )
                if price_element:
                    price_text = price_element.get_text().strip().translate(AR)
                    price_str = ''.join(c for c in price_text if c.isdigit() or c == '.')
                    if price_str:
                        current_price = float(price_str)
            
            if current_price:
                checked_count += 1
                is_new_product = url not in stored_data
                
                if is_new_product:
                    stored_data[url] = {
                        "name": product_name,
                        "current_price": current_price,
                        "history": [{"price": current_price, "time": current_time_str}]
                    }
                else:
                    item_data = stored_data[url]
                    old_price = item_data["current_price"]
                    
                    if current_price != old_price:
                        prices_list = [h["price"] for h in item_data["history"]]
                        prices_list.append(current_price)
                        avg_price = round(sum(prices_list) / len(prices_list), 2)
                        lowest_historical_price = min(prices_list[:-1]) if len(prices_list) > 1 else old_price
                        
                        if current_price < old_price:
                            diff_pct = round(((old_price - current_price) / old_price) * 100, 1)
                            discount_text = f"📉 نسبة الخصم: %{diff_pct}"
                        else:
                            diff_pct = round(((current_price - old_price) / old_price) * 100, 1)
                            discount_text = f"📈 نسبة الزيادة: %{diff_pct}"
                        
                        is_lowest = current_price <= lowest_historical_price
                        tagline = "🔥 أقل سعر تاريخي!" if is_lowest else "📊 تحديث جديد في السعر"
                        
                        item_data["current_price"] = current_price
                        item_data["name"] = product_name
                        item_data["history"].append({"price": current_price, "time": current_time_str})
                        
                        history_text = ""
                        for h in reversed(item_data["history"][-5:]):
                            history_text += f"➡️ EGP {h['price']} – {h['time']}\n"
                        
                        msg = (
                            f"✨ عرض كنز ✨\n\n"
                            f"🛒 {product_name}\n\n"
                            f"💵 السعر الحالي: EGP {current_price}\n"
                            f"💵 السعر السابق: EGP {old_price}\n"
                            f"📊 متوسط الأسعار: EGP {avg_price}\n"
                            f"{discount_text}\n"
                            f"{tagline}\n\n"
                            f"📜 تاريخ الأسعار:\n"
                            f"{history_text}\n"
                            f"🛍️ **رابط المنتج:**\n{url}\n\n"
                            f"🔗 [اضغط هنا للشراء مباشرة]({url})"
                        )
                        send(msg)
                        changes_count += 1
                
                print(f"[{index}/{total_products_count}] ✅ تم الفحص - {product_name} | السعر: {current_price}")
            else:
                print(f"[{index}/{total_products_count}] ⚠️ لم يتم العثور على السعر.")
            
            time.sleep(1.5)
            
        except Exception as e:
            print(f"[{index}/{total_products_count}] ❌ خطأ: {e}")
            
    save_data(stored_data)
    print(f"\n[⏳] انتهت الدورة الحالية (تم فحص {checked_count} منتج، رصد {changes_count} تغيير).")

if __name__ == "__main__":
    print("البوت يعمل الآن في الخلفية لمراقبة الأسعار بصمت...")
    while True:
        check_prices()
        time.sleep(900)
