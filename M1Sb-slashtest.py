#
# Kode stump til at illustrere forskel med backslash "\" og forwardslash "/"
#
# Det ser umiddelbart meget tilforladeligt ud. MEN bemærk udskriften for t6
#   - Ikke som forventet - bachslach forsvinder!!!
#   - Det er fordi \b tolkes som et special tegn - som backspace BS!!!!
#
# Og bemærk også udskrift for t13-t18
#   - Der kommer kun een backslash i alle udskrifter selvom der står to efter hinanden i konstanterne! 
#
# Bemærk som det sidste at det kan ikke lade sig gøre at slutte med backslash
#  - så får man en fejl - prøv det!!
#
#
# Konklusion - Brug forwardslash eller dobbelt backslash i sti navne!!
#
# Hvorfor kommer man til at bruge backslash?
#   - Fordi det er det man får når man kopierer sti navn i fil/folder system på PC!
#      - med shift/right mouse click og kopier sti..
#   - Er det forward- eller backslash i de forskellige metoder på MAC?
# Hvorfor virker det nogle gange med enkelt backslash?
#   - Fordi det afhænger af det tegn/bogstav som kommer efter!
#   - se hvilke i https://docs.python.org/2.0/ref/strings.html
#

t1  = "tekst streng med backslash \ efterfulgt af space"          
t2  = "tekst streng med backslash \L efterfulgt af L som i LKM1"
t3  = "tekst streng med backslash \l efterfulgt af l som i lyde"
t4  = "tekst streng med backslash \d efterfulgt af d som i div"
t5  = "tekst streng med backslash \h efterfulgt af h som i hej-ol"   
t6  = "tekst streng med backslash \b efterfulgt af b som i baggrund"   

t7  = "tekst streng med forwardslash / efterfulgt af space"         
t8  = "tekst streng med forwardslash /L efterfulgt af L som i LKM1"
t9  = "tekst streng med forwardslash /l efterfulgt af l som i lyde"
t10 = "tekst streng med forwardslash /d efterfulgt af d som i div"
t11 = "tekst streng med forwardslash /h efterfulgt af h som i hej-ol"   
t12 = "tekst streng med forwardslash /b efterfulgt af b som i baggrund"

t13 = "tekst streng med dobbelt backslash \\ efterfulgt af space"          
t14 = "tekst streng med dobbelt backslash \\L efterfulgt af L som i LKM1"
t15 = "tekst streng med dobbelt backslash \\l efterfulgt af l som i lyde"
t16 = "tekst streng med dobbelt backslash \\d efterfulgt af d som i div"
t17 = "tekst streng med dobbelt backslash \\h efterfulgt af h som i hej-ol"   
t18 = "tekst streng med dobbelt backslash \\b efterfulgt af b som i baggrund"

nl = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18]

for i in range(len(nl)):
    print("t",i+1,": ",nl[i])