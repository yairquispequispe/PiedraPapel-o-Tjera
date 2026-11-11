import random
import sqlite3

conexion = sqlite3.connect("piedra_papel_tijera.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS partidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_jugador TEXT,
    eleccion_jugador TEXT,
    eleccion_computadora TEXT,
    resultado TEXT
)
""")
conexion.commit()

print("¡Bienvenido al juego de Piedra, Papel o Tijera con SQLite3!")

nombre = input("Por favor, escribe tu nombre: ").strip()
if not nombre:
    nombre = "Jugador"

opciones = ["piedra", "papel", "tijera"]

seguir = "s"
while seguir.lower() == "s":
    
    jugador = ""
    while jugador not in opciones:
        jugador = input("\nElige (piedra, papel, tijera): ").lower().strip()
    
    computadora = random.choice(opciones)
    print(f"La computadora eligió: {computadora}")
    
    if jugador == computadora:
        resultado = "Empate"
    elif (jugador == "piedra" and computadora == "tijera") or \
         (jugador == "papel" and computadora == "piedra") or \
         (jugador == "tijera" and computadora == "papel"):
        resultado = "Ganaste"
    else:
        resultado = "Perdiste"
        
    print(f"Resultado de la partida: ¡{resultado}!")
    
    cursor.execute("""
    INSERT INTO partidas (nombre_jugador, eleccion_jugador, eleccion_computadora, resultado)
    VALUES (?, ?, ?, ?)
    """, (nombre, jugador, computadora, resultado))
    conexion.commit()
    
    seguir = input("\n¿Quieres jugar otra partida? (s/n): ").strip()

print(f"\n--- ESTADÍSTICAS FINALES PARA {nombre.upper()} ---")

cursor.execute("SELECT COUNT(*) FROM partidas WHERE nombre_jugador = ? AND resultado = 'Ganaste'", (nombre,))
victorias = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM partidas WHERE nombre_jugador = ? AND resultado = 'Perdiste'", (nombre,))
derrotas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM partidas WHERE nombre_jugador = ? AND resultado = 'Empate'", (nombre,))
empates = cursor.fetchone()[0]

print(f" Victorias: {victorias}")
print(f" Derrotas: {derrotas}")
print(f" Empates: {empates}")
print(f" Total de partidas registradas: {victorias + derrotas + empates}")

conexion.close()
print("\n¡Gracias por jugar! Tu historial ha sido guardado.")
