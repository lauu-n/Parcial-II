import mesa
import numpy as np
import random

class PerceptronAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Inicializar pesos aleatorios (2 entradas + bias)
        self.weights = np.random.uniform(-1, 1, 3)
        self.learning_rate = self.model.learning_rate
        self.errors = []
        
    def step(self):
        """Un paso de entrenamiento del perceptrón"""
        if self.model.current_iteration < self.model.max_iterations:
            # Seleccionar un punto aleatorio
            idx = random.randint(0, len(self.model.training_data) - 1)
            point, target = self.model.training_data[idx]
            
            # Realizar predicción
            prediction = self.predict(point)
            
            # Calcular error
            error = target - prediction
            
            # Actualizar pesos si hay error
            if error != 0:
                self.weights[0] += self.learning_rate * error * point[0]  # w1
                self.weights[1] += self.learning_rate * error * point[1]  # w2
                self.weights[2] += self.learning_rate * error * 1         # bias
            
            self.errors.append(abs(error))
            self.model.current_iteration += 1
    
    def predict(self, point):
        """Predecir la clase de un punto"""
        inputs = np.array([point[0], point[1], 1])  # Agregar bias
        summation = np.dot(self.weights, inputs)
        return 1 if summation >= 0 else -1
    
    def get_decision_boundary(self):
        """Obtener parámetros de la línea de decisión: w1*x + w2*y + bias = 0"""
        return self.weights[0], self.weights[1], self.weights[2]

class DataPoint(mesa.Agent):
    def __init__(self, unique_id, model, pos, true_label):
        super().__init__(unique_id, model)
        self.pos = pos
        self.true_label = true_label
        self.predicted_label = None
        self.is_correct = False
        
    def step(self):
        """Actualizar clasificación del punto"""
        perceptron = self.model.schedule.agents[0]  # El primer agente es el perceptrón
        if isinstance(perceptron, PerceptronAgent):
            self.predicted_label = perceptron.predict(self.pos)
            self.is_correct = (self.predicted_label == self.true_label)

class PerceptronModel(mesa.Model):
    def __init__(self, num_points=50, learning_rate=0.1, max_iterations=100):
        super().__init__()
        self.num_points = num_points
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.training_complete = False
        
        # Crear scheduler
        self.schedule = mesa.time.RandomActivation(self)
        
        # Crear el perceptrón
        perceptron = PerceptronAgent(0, self)
        self.schedule.add(perceptron)
        
        # Generar datos de entrenamiento
        self.training_data = self.generate_linear_data()
        
        # Crear puntos de datos visuales
        self.create_visual_points()
        
        # Data collector para métricas
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Accuracy": "accuracy",
                "Error": "current_error",
                "Iteration": "current_iteration"
            }
        )
    
    def generate_linear_data(self):
        """Generar datos linealmente separables"""
        data = []
        # Línea de separación real: y = 0.5*x + 3
        for _ in range(self.num_points):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            
            if y > 0.5*x + 3:  # Por encima de la línea
                true_label = 1
            else:              # Por debajo de la línea
                true_label = -1
                
            data.append(((x, y), true_label))
        return data
    
    def create_visual_points(self):
        """Crear agentes para visualización"""
        for i, (point, true_label) in enumerate(self.training_data, 1):
            point_agent = DataPoint(i, self, point, true_label)
            self.schedule.add(point_agent)
    
    def step(self):
        """Avanzar la simulación un paso"""
        if not self.training_complete:
            self.schedule.step()
            self.datacollector.collect(self)
            
            # Verificar si completó el entrenamiento
            if self.current_iteration >= self.max_iterations:
                self.training_complete = True
                print("¡Entrenamiento completado!")
                print(f"Precisión final: {self.accuracy:.2%}")
    
    @property
    def accuracy(self):
        """Calcular precisión actual"""
        correct = 0
        total = 0
        
        for agent in self.schedule.agents:
            if isinstance(agent, DataPoint):
                total += 1
                if agent.is_correct:
                    correct += 1
        
        return correct / total if total > 0 else 0
    
    @property
    def current_error(self):
        """Obtener error actual del perceptrón"""
        perceptron = self.schedule.agents[0]
        if isinstance(perceptron, PerceptronAgent) and perceptron.errors:
            return perceptron.errors[-1]
        return 0
    
    def reset_model(self, new_learning_rate=None, new_max_iterations=None):
        """Reiniciar el modelo con nuevos parámetros"""
        if new_learning_rate is not None:
            self.learning_rate = new_learning_rate
        if new_max_iterations is not None:
            self.max_iterations = new_max_iterations
            
        # Reiniciar variables
        self.current_iteration = 0
        self.training_complete = False
        
        # Limpiar y recrear agents
        self.schedule = mesa.time.RandomActivation(self)
        
        # Nuevo perceptrón
        perceptron = PerceptronAgent(0, self)
        self.schedule.add(perceptron)
        
        # Nuevos puntos de datos
        self.training_data = self.generate_linear_data()
        self.create_visual_points()

def agent_portrayal(agent):
    portrayal = {"Filled": "true"}
    
    if isinstance(agent, DataPoint):
        # Puntos más grandes para mejor visualización
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.4
        portrayal["Layer"] = 1
        
        # Color según clasificación
        if agent.predicted_label is None:
            portrayal["Color"] = "gray"  # Sin clasificar
        elif agent.is_correct:
            portrayal["Color"] = "green"  # Correcto
        else:
            portrayal["Color"] = "red"    # Incorrecto
            
    elif isinstance(agent, PerceptronAgent):
        # Representar el perceptrón (no visible en la grid)
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
        portrayal["w"] = 0.1
        portrayal["h"] = 0.1
        portrayal["Layer"] = 0
        
    return portrayal

# Crear la grid de visualización
grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Crear gráficos
chart_error = mesa.visualization.ChartModule([
    {"Label": "Error", "Color": "red"}
])

chart_accuracy = mesa.visualization.ChartModule([
    {"Label": "Accuracy", "Color": "green"}
])

# Parámetros del modelo
model_params = {
    "num_points": mesa.visualization.Slider(
        "Número de puntos", 
        50, 10, 100, 1,
        description="Cantidad de puntos de entrenamiento"
    ),
    "learning_rate": mesa.visualization.Slider(
        "Tasa de aprendizaje", 
        0.1, 0.01, 1.0, 0.01,
        description="Tasa de aprendizaje del perceptrón"
    ),
    "max_iterations": mesa.visualization.Slider(
        "Iteraciones máximas", 
        100, 10, 500, 10,
        description="Número máximo de iteraciones de entrenamiento"
    )
}

# Crear el servidor
server = mesa.visualization.ModularServer(
    PerceptronModel,
    [grid, chart_error, chart_accuracy],
    "Perceptrón con MESA",
    model_params
)

# Ejecutar directamente
if __name__ == "__main__":
    print("Iniciando simulación del Perceptrón...")
    print("Abre tu navegador en: http://127.0.0.1:8521/")
    server.port = 8521
    server.launch()