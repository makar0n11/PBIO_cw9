
import random  # Importujemy bibliotekę random do losowania nukleotydów i miejsca wstawienia imienia
import textwrap  # Importujemy do łamania linii w zapisie FASTA (ULEPSZENIE 1)

# Funkcja do generowania losowej sekwencji DNA
def generate_dna_sequence(length):
    # Zwraca losowy ciąg znaków A, C, G, T o zadanej długości
    return ''.join(random.choices('ACGT', k=length))

# Funkcja do wstawiania imienia w losowym miejscu sekwencji
def insert_name(sequence, name):
    pos = random.randint(0, len(sequence))  # Losujemy miejsce wstawienia
    return sequence[:pos] + name + sequence[pos:]  # Wstawiamy imię w tym miejscu

# Funkcja do obliczania statystyk sekwencji (bez imienia)
def calculate_stats(sequence, name):
    # Usuwamy imię, żeby nie zaburzyło statystyk
    clean_sequence = sequence.replace(name, '')
    length = len(clean_sequence)  # Obliczamy długość sekwencji czystej
    stats = {
        nuc: round((clean_sequence.count(nuc) / length) * 100, 1) for nuc in 'ACGT'
    }  # Liczymy % zawartości każdego nukleotydu
    cg = clean_sequence.count('C') + clean_sequence.count('G') #c+g
    at = clean_sequence.count('A') + clean_sequence.count('T') #a+t
    # Obliczamy stosunek CG do całkowitej liczby zasad (w procentach)
    cg_ratio = round((cg / (at + cg)) * 100, 1) if (at + cg) > 0 else 0
    return stats, cg_ratio

# Funkcja do zapisu sekwencji w formacie FASTA
def save_to_fasta(filename, header, sequence):
    # ORIGINAL:
    # with open(filename, 'w') as f:
    #     f.write(f">{header}\n{sequence}\n")
    # MODIFIED (dodano łamanie linii co 60 znaków dla zgodności z konwencją FASTA):
    with open(filename, 'w') as f:
        f.write(f">{header}\n")
        wrapped = textwrap.fill(sequence, width=60)  # Łamie sekwencję co 60 znaków
        f.write(f"{wrapped}\n")  # Zapisuje sekwencję

# Funkcja główna programu
def main():
    try:
        # ORIGINAL:
        # length = int(input("Podaj długość sekwencji: "))
        # MODIFIED (dodano walidację danych wejściowych - ULEPSZENIE 2):
        length_input = input("Podaj długość sekwencji: ")
        if not length_input.isdigit() or int(length_input) <= 0:
            raise ValueError("Długość musi być dodatnią liczbą całkowitą.")
        length = int(length_input)

        # Pobieranie pozostałych danych od użytkownika
        seq_id = input("Podaj ID sekwencji: ").strip()
        description = input("Podaj opis sekwencji: ").strip()
        name = input("Podaj imię: ").strip()

        # ORIGINAL:
        # dna = generate_dna_sequence(length)
        # dna_with_name = insert_name(dna, name)
        # MODIFIED (dodanie informacji o położeniu imienia w sekwencji ):
        dna = generate_dna_sequence(length)
        pos = random.randint(0, len(dna))  # Wylosuj miejsce wstawienia imienia
        dna_with_name = dna[:pos] + name + dna[pos:]
        print(f"(Imię '{name}' wstawiono na pozycję {pos})")  # Informacja diagnostyczna

        # Przygotowanie nagłówka FASTA i nazwy pliku
        header = f"{seq_id} {description}"
        filename = f"{seq_id}.fasta"

        # Zapis do pliku
        save_to_fasta(filename, header, dna_with_name)
        print(f"\nSekwencja została zapisana do pliku {filename}")

        # Obliczanie statystyk i ich wyświetlenie
        stats, cg_ratio = calculate_stats(dna_with_name, name)
        print("Statystyki sekwencji:")
        for nuc in 'ACGT':
            print(f"{nuc}: {stats[nuc]}%")
        print(f"%CG: {cg_ratio}")

    except ValueError as e:
        print(f"Błąd: {e}")  # Obsługa błędu wprowadzania danych

# Uruchomienie programu, jeśli plik wykonywany jest bezpośrednio
if __name__ == "__main__":
    main()