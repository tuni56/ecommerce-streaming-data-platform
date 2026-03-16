# Demo Runbook — Ecommerce Streaming Platform

## Arquitectura

```
Producer (Python) → Kafka 3.9 KRaft → Consumer (Python)
                                     → Spark 4.1 Streaming (agregaciones)
Todo corre dentro del contenedor LXD: ecommerce-streaming (10.34.23.19)
```

---

## 1. Arrancar todo

```bash
bash scripts/start-demo.sh
```

Verifica que Kafka esté corriendo y los topics existan. Al final imprime los comandos para cada terminal.

---

## 2. Abrir la demo en tmux

```bash
tmux
```

### Atajos tmux esenciales

| Acción | Teclas |
|--------|--------|
| Dividir vertical | `Ctrl+B` luego `%` |
| Dividir horizontal | `Ctrl+B` luego `"` |
| Moverse entre paneles | `Ctrl+B` luego `o` |
| Salir sin cerrar nada | `Ctrl+B` luego `D` |
| Volver a tmux | `tmux attach` |

### Layout recomendado para la charla

```
┌─────────────────────┬─────────────────────┐
│   Terminal 1        │   Terminal 2         │
│   PRODUCER          │   CONSUMER           │
│                     ├──────────────────────┤
│                     │   Terminal 3         │
│                     │   SPARK              │
└─────────────────────┴──────────────────────┘
```

Pasos:
1. `tmux` — entrás
2. `Ctrl+B %` — dividís vertical (izq/der)
3. Panel izquierdo → pegás Terminal 1
4. `Ctrl+B o` — vas al panel derecho
5. `Ctrl+B "` — dividís horizontal (arriba/abajo)
6. Panel superior derecho → pegás Terminal 2
7. `Ctrl+B o` — vas al panel inferior derecho
8. Panel inferior derecho → pegás Terminal 3

---

## 3. Comandos de cada terminal

### Terminal 1 — Producer
```bash
lxc exec ecommerce-streaming -- /opt/ecommerce-venv/bin/python /tmp/producer.py
```

### Terminal 2 — Consumer Python
```bash
lxc exec ecommerce-streaming -- /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic page_views --from-beginning
```

### Terminal 3 — Spark Streaming
```bash
lxc exec ecommerce-streaming -- sh -c '
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PYSPARK_PYTHON=/opt/ecommerce-venv/bin/python
JARS=/opt/spark-jars/spark-sql-kafka-0-10_2.13-4.1.0.jar,/opt/spark-jars/kafka-clients-3.8.0.jar,/opt/spark-jars/spark-token-provider-kafka-0-10_2.13-4.1.0.jar,/opt/spark-jars/commons-pool2-2.12.0.jar
/opt/ecommerce-venv/lib/python3.12/site-packages/pyspark/bin/spark-submit --jars $JARS /tmp/spark_job.py'
```

---

## 4. Apagar todo

```bash
# 1. Detener procesos en cada panel de tmux
Ctrl+C

# 2. Salir de tmux
Ctrl+B luego D

# 3. Detener Kafka
lxc exec ecommerce-streaming -- sh -c 'kill $(cat /var/run/kafka.pid)'

# 4. Apagar el contenedor
lxc stop ecommerce-streaming

# Verificar
lxc list   # debe mostrar ecommerce-streaming en STOPPED
```

---

## 5. Versiones del stack

| Componente | Versión |
|------------|---------|
| LXD | 5.21.4 |
| Ubuntu (container) | 24.04 |
| Java | OpenJDK 17 |
| Kafka | 3.9.0 KRaft |
| Python | 3.12 |
| uv | 0.10.10 |
| kafka-python | 2.3.0 |
| PySpark | 4.1.1 |
| spark-sql-kafka connector | 4.1.0 |

---

## 6. Troubleshooting

**Kafka no arranca**
```bash
lxc exec ecommerce-streaming -- tail -20 /var/log/kafka.log
```

**Topics no existen**
```bash
lxc exec ecommerce-streaming -- sh -c '
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092'
```

**Spark no encuentra el datasource kafka**
Verificar que los jars estén en `/opt/spark-jars/` dentro del contenedor:
```bash
lxc exec ecommerce-streaming -- ls /opt/spark-jars/
```

**El contenedor no tiene internet**
Normal. Todos los binarios ya están instalados dentro. No necesita internet para correr.

---

*Build on, always. I design, therefore I exist.*
