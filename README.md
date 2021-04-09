# SMP-2021


## Obiectiv Proiect:
Integrarea modulelor de simulare si generare a instructiunilor assembly pe arhitectura x86 32bit intr-o interfata grafica usor de utilizat.
## Functionalitati:
- Afisarea valorilor din registrele de uz general
- Rularea instructiunilor simple de calcul pe baza valorilor din registrele generale
- Rularea instructiunilor ce permit utilizarea memoriei
- Afisarea valorilor flag-urilor
- Afisarea memoriei
### Ce am implementat pana in acest moment - [aici](https://youtu.be/cifu8zb8CDI)
## Alte simulatoare:
1. [Carlosrafaelgn’s simulator](https://carlosrafaelgn.com.br/asm86/) - permite rularea unui set de instructiuni assembly pe x86 cu facilitatea de urmarire a valorilor din registrele generale, dar si a flag-urilor, codul assembly scris are o executie oneshot, adica la apasarea butonului run se executa codul si obtinem rezultatul, la o apasare ulterioara fara resetarea simulatorului nu se intampla nimic
2. [Davis simulator](https://kobzol.github.io/davis/) - permite rularea unui intreg program assembly, alaturi de vizualizarea valorilor registrilor de uz general, a flag-urilor si a valorilor din memoria RAM, cu posibilitatea de grupare a memoriei in blocuri de 1, 2 sau chiar 4 octeti
3. [Schweigi’s simulator](https://schweigi.github.io/assembler-simulator/) - este un simulator pe 8 biti, cu un numar mai redus de registre generale, dar in schimb prezinta facilitati mai interesante pe partea de simulare, highlight pe instructiunea ce ruleaza la un anumit moment de timp
4. [Marss simulator](https://github.com/avadhpatel/marss) - nu am reusit sa-l rulez


## Module de baza:
[Unicorn](https://www.unicorn-engine.org/)
[Keystone](https://www.keystone-engine.org/)
[Tkinter](https://docs.python.org/3/library/tkinter.html)

## Aplicatii utile:
[Dezasamblor](https://onlinedisassembler.com/odaweb/)
[x86 opcode](http://ref.x86asm.net/coder32.html)




