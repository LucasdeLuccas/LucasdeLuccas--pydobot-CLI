from colorama import Fore, Back
from serial.tools import list_ports
import inquirer
import pydobot
import yaspin

# Define a instância de carregamento e a introdução do programa
loading = yaspin.yaspin(text="Em andamento...", color="green")

print(Back.LIGHTBLACK_EX + Fore.YELLOW + "Agora você está usando a CLI! Avanti Palestra!")
print("Este programa foi desenvolvido para controlar o robô Dobot Magician.")
print(Back.BLACK + Fore.WHITE + "\nSelecione a porta USB em que o robô esta conectado.")

# Funções de ação do robô
def home():
    #Move a garra para a posição inicial.
    loading.start()
    robot.move_to(200, 0, 0, 0)
    loading.stop()
    mainMenu()

def ligar_ferramenta():
    #Ativa a ferramenta do robô.
    robot.suck(True)
    mainMenu()

def desligar_ferramenta():
   #Desativa a ferramenta do robô.
    robot.suck(False)
    mainMenu()

def mover(axys: str, distance: float):
    #Move a garra em um eixo especificado por uma distância dada.
    current_position = robot.pose()
    loading.start()
    match axys:
        case "x":
            robot.move_to(distance, *current_position[1:])
        case "y":
            robot.move_to(current_position[0], distance, *current_position[2:])
        case "z":
            robot.move_to(*current_position[:2], distance, current_position[3])
        case "r":
            robot.move_to(*current_position[:3], distance)
    loading.stop()
    mainMenu()

def atual():
    #Exibe e retorna a posição atual da garra.
    print("\n\nPosição atual do robô:\n" + "\n".join([f" {axis}:{pos}" for axis, pos in zip("XYZR", robot.pose())]))
    mainMenu()

# Menu principal do programa
def mainMenu():
    
    acoes = ["Home", "Ligar ferramenta", "Desligar ferramenta", "Mover", "Posição atual", "Sair da aplicação"]
    chosenAction = inquirer.prompt([inquirer.List("action", message="MENU PRINCIPAL\nSelecione uma ação", choices=acoes)])
    
    match chosenAction["action"]:
        case "Home": home()
        case "Ligar ferramenta": ligar_ferramenta()
        case "Desligar ferramenta": desligar_ferramenta()
        case "Mover":
            axys = input("Eixo (x, y, z, r): ")
            distance = float(input("Distância: "))
            mover(axys, distance)
        case "Posição atual": atual()
        case "Sair da aplicação": 
            robot.close()
            exit()

# Conexão e inicialização do robô
connectedUsbPorts = list_ports.comports()
chosenUsbPort = inquirer.prompt([inquirer.List("port", message="Selecione a porta:", choices=[port.device for port in connectedUsbPorts])])["port"]

robot = pydobot.Dobot(port=chosenUsbPort)
robot.speed(200, 200)

mainMenu()
