import html
import string
import asyncio
from Script import text
from .database import tb
from config import LOG_CHANNEL
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ABC = string.ascii_lowercase + string.ascii_uppercase
NUM = string.digits
PAGE, COLS, MAX_LEN, OUTPUT_MAX_LEN = 21, 3, 1000, 3500
ORIGINAL_TEXTS = {}

STYLES = {
    "cool": ("Italic Serif", "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍", "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫", ""),
    "serif": ("Bold Serif", "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗", ""),
    "bold_cool": ("Bold Italic Serif", "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗", ""),
    "sim": ("Sans Serif", "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹", "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫", ""),
    "slant": ("Italic Sans", "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡", "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫", ""),
    "sans": ("Bold Sans", "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "slant_sans": ("Bold Italic Sans", "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "script": ("Script", "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡", ""),
    "script_bold": ("Bold Script", "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗", ""),
    "gothic": ("Fraktur", "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗", ""),
    "bold_fraktur": ("Bold Fraktur", "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗", ""),
    "outline": ("Double-Struck", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡", ""),
    "typewriter": ("Typewriter", "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿", ""),
    "fullwidth": ("Fullwidth", "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ", "０１２３４５６７８９", ""),
    "small_cap": ("Small Caps", "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿", ""),
    "tiny": ("Tiny", "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ", "⁰¹²³⁴⁵⁶⁷⁸⁹", ""),
    "superscript": ("Superscript", "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𐞥ʳˢᵗᵘᵛʷˣʸᶻᴬᴮꟲᴰᴱꟳᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾꟴᴿˢᵀᵁⱽᵂˣʸᶻ", "⁰¹²³⁴⁵⁶⁷⁸⁹", ""),
    "subscript": ("Subscript", "ₐᵦ꜀ᵈₑբɡₕᵢⱼₖₗₘₙₒₚᵩᵣₛₜᵤᵥwₓᵧzₐᵦ꜀ᵈₑբɡₕᵢⱼₖₗₘₙₒₚᵩᵣₛₜᵤᵥwₓᵧz", "₀₁₂₃₄₅₆₇₈₉", ""),
    "bubbles": ("Bubbles", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ", "⓪①②③④⑤⑥⑦⑧⑨", "\ufe0e"),
    "dark_bubbles": ("Dark Bubbles", "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩", "⓿➊➋➌➍➎➏➐➑➒", "\ufe0e"),
    "squares": ("Squares", "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "dark_squares": ("Dark Squares", "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉", "⓿➊➋➌➍➎➏➐➑➒", "\ufe0e"),
    "parentheses": ("Enclosed", "", "⓪①②③④⑤⑥⑦⑧⑨", "\u20dd"),
    "comic": ("Comic", "ᗩᗷᑕᗪᗴᖴᘜᕼIᒍKᒪᗰᑎOᑭᑫᖇՏTᑌᐯᗯ᙭YᘔᗩᗷᑕᗪᗴᖴᘜᕼIᒍKᒪᗰᑎOᑭᑫᖇՏTᑌᐯᗯ᙭Yᘔ", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "andalucia": ("Andalucia", "ꪖ᥇ᥴᦔꫀᠻᧁꫝ𝓲𝓳𝘬ꪶꪑꪀꪮρ𝘲𝘳𝘴𝓽ꪊꪜ᭙᥊ꪗɀꪖ᥇ᥴᦔꫀᠻᧁꫝ𝓲𝓳𝘬ꪶꪑꪀꪮρ𝘲𝘳𝘴𝓽ꪊꪜ᭙᥊ꪗɀ", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "ladybug": ("Ladybug", "ꍏꌃꏳꀷꏂꎇꁅꀍꀤ꒻ꀘ꒒ꎭꈤꂦᖘꆰꋪꌚ꓄ꀎ꒦ꅐꉧꌩꁴꍏꌃꏳꀷꏂꎇꁅꀍꀤ꒻ꀘ꒒ꎭꈤꂦᖘꆰꋪꌚ꓄ꀎ꒦ꅐꉧꌩꁴ", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "manga": ("Manga", "卂乃匚ᗪ乇千ᘜ卄|ﾌҜㄥ爪几ㄖ卩Ҩ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千ᘜ卄|ﾌҜㄥ爪几ㄖ卩Ҩ尺丂ㄒㄩᐯ山乂ㄚ乙", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "qvnes": ("Qvnes", "ልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊ", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "currency": ("Currency", "₳฿₵ĐɆ₣₲ⱧŁJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ₳฿₵ĐɆ₣₲ⱧŁJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "stroke": ("Stroke", "ⱥƀȼđɇfǥħɨɉꝁłmnøᵽꝗɍsŧᵾvwxɏƶȺɃȻĐɆFǤĦƗɈꝀŁMNØⱣꝖɌSŦɄVWXɎƵ", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "thai": ("Thai", "ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչ", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "greek": ("Greek", "αႦçԃεƒɠɦιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥαႦçԃεƒɠɦιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "japan": ("Japan", "ﾑ乃ᄃり乇ｷムんﾉﾌズﾚﾶ刀のｱゐ尺ㄎｲひ√Wﾒﾘ乙ﾑ乃ᄃり乇ｷムんﾉﾌズﾚﾶ刀のｱゐ尺ㄎｲひ√Wﾒﾘ乙", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "cyrillic": ("Cyrillic", "ДБҀↁЄҒԌНІЈЌĿМИФРԚЯЅГЦѴШЖЧƵДБҀↁЄҒԌНІЈЌĿМИФРԚЯЅГЦѴШЖЧƵ", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", ""),
    "runes": ("Runes", "ᚨᛒᚳᛞᛖᚠᚷᚺᛁᛃᚴᛚᛗᚾᛟᛈᛩᚱᛊᛏᚢᚡᚹᛪᚤᛉᚨᛒᚳᛞᛖᚠᚷᚺᛁᛃᚴᛚᛗᚾᛟᛈᛩᚱᛊᛏᚢᚡᚹᛪᚤᛉ", "⓪①②③④⑤⑥⑦⑧⑨", ""),
    "special": ("Flags", "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u200a"),
    "cloud": ("Clouds", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0361\u035c"),
    "happy": ("Happy", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0306\u0308"),
    "sad": ("Sad", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0311\u0308"),
    "stinky": ("Stinky", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u033e"),
    "bubble_marks": ("Bubble Marks", "", "⓪①②③④⑤⑥⑦⑧⑨", "\u0366\u0325"),
    "underline": ("Underline", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u035f"),
    "rays": ("Rays", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0489"),
    "birds": ("Birds", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0488"),
    "slash": ("Slash", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0338"),
    "stop": ("Stop", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u20e0"),
    "skyline": ("Skyline", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0346\u033a"),
    "arrows": ("Arrows", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u034e"),
    "strike": ("Strikethrough", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0336"),
    "frozen": ("Frozen", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0f19"),
    "dotted": ("Dotted", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0307"),
    "dot_below": ("Dot Below", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0323"),
    "wavy": ("Wavy", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0330"),
    "overline": ("Overline", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0305"),
    "double_line": ("Double Underline", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0332\u0332"),
    "tilde": ("Tilde", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0303"),
    "glitch": ("Glitch", "", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵", "\u0300\u0353\u0346\u0318\u0357\u032d"),
}


TABLES = {
    key: str.maketrans({
        **{char: output + suffix for char, output in zip(ABC, letters or ABC)},
        **{char: output + suffix for char, output in zip(NUM, digits)},
    })
    for key, (_, letters, digits, suffix) in STYLES.items()
}


def convert(key, value):
    return value.translate(TABLES[key])


def build_keyboards():
    keys = list(STYLES)
    pages = [keys[i:i + PAGE] for i in range(0, len(keys), PAGE)]
    boards = []
    for page_num, page in enumerate(pages):
        buttons = [InlineKeyboardButton(convert(key, STYLES[key][0]), callback_data=f"fs:{key}") for key in page]
        rows = [buttons[i:i + COLS] for i in range(0, len(buttons), COLS)]
        nav = []
        if page_num:
            nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"fp:{page_num - 1}"))
        if page_num < len(pages) - 1:
            nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"fp:{page_num + 1}"))
        if nav:
            rows.append(nav)
        boards.append(InlineKeyboardMarkup(rows))
    return boards


KB = build_keyboards()


def get_message_text(message):
    return (message.text or message.caption) if message else None


def get_original_text(bot_msg):
    cached = ORIGINAL_TEXTS.get((bot_msg.chat.id, bot_msg.id))
    if cached is not None:
        return cached[:MAX_LEN]
    original = bot_msg.reply_to_message
    raw = get_message_text(original)
    if not raw:
        return None
    parts = raw.split(maxsplit=1)
    command = parts[0].split("@", 1)[0] if parts else ""
    if command == "/font":
        if len(parts) > 1:
            return parts[1][:MAX_LEN]
        replied = get_message_text(original.reply_to_message)
        return replied[:MAX_LEN] if replied else None
    return raw[:MAX_LEN]


async def log_new_user(client, message):
    user = message.from_user
    if not user:
        return
    try:
        if await tb.get_user(user.id) is not None:
            return
        await tb.add_user(user.id, user.first_name or "N/A")
        bot = await client.get_me()
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(user.id, getattr(user, "dc_id", "N/A"),
                            user.first_name or "N/A",
                            f"@{user.username}" if user.username else "N/A",
                            bot.username)
        )
    except Exception as error:
        print(f"User logging error: {error}")


@Client.on_message((filters.private & filters.text & ~filters.regex(r"^/")) | (filters.private & filters.command("font")))
async def font_cmd(client, message):
    raw = get_message_text(message) or ""
    parts = raw.split(maxsplit=1)
    command = parts[0].split("@", 1)[0] if parts else ""
    if command == "/font":
        user_text = parts[1] if len(parts) > 1 else None
        if not user_text:
            user_text = get_message_text(message.reply_to_message)
    else:
        user_text = raw
        await log_new_user(client, message)
    if not user_text:
        return await message.reply_text("Enter any text. Eg: <code>/font Hello</code>", parse_mode=ParseMode.HTML)
    user_text = user_text[:MAX_LEN]
    reply = await message.reply_text(html.escape(user_text), reply_markup=KB[0], parse_mode=ParseMode.HTML)
    ORIGINAL_TEXTS[(reply.chat.id, reply.id)] = user_text
    asyncio.create_task(auto_delete_messages(client, message.chat.id, message.id, reply.id))


async def auto_delete_messages(client, chat_id, *message_ids):
    await asyncio.sleep(300)
    try:
        await client.delete_messages(chat_id, list(message_ids))
    except Exception as error:
        print(f"Auto-delete error: {error}")
