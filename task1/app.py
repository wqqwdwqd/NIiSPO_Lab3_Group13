import os  # 读取环境变量
from flask import Flask, jsonify  # 创建 Web 应用和 JSON 响应
from opentelemetry import trace  # OpenTelemetry 追踪接口
from opentelemetry.sdk.resources import Resource  # 定义服务信息
from opentelemetry.sdk.trace import TracerProvider  # 管理追踪数据
from opentelemetry.sdk.trace.export import BatchSpanProcessor  # 批量发送 Span
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter  # OTLP HTTP 导出器
from opentelemetry.instrumentation.flask import FlaskInstrumentor  # Flask 自动追踪

# 为 Jaeger 中的服务指定可辨识名称
resource = Resource.create({'service.name': 'lab3-flask-group13'})
provider = TracerProvider(resource=resource)
# 发送到 Docker 网络中的 Jaeger OTLP 接口
exporter = OTLPSpanExporter(endpoint=os.getenv('OTEL_EXPORTER_OTLP_TRACES_ENDPOINT', 'http://jaeger:4318/v1/traces'))
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)  # 创建 Flask 应用
FlaskInstrumentor().instrument_app(app)  # 追踪每个 HTTP 请求

@app.get('/')
def home():
    with tracer.start_as_current_span('prepare-welcome-message') as span:
        span.set_attribute('lab.group', 13)
        return jsonify(message='Hello from Flask with OpenTelemetry', group=13, laboratory=3)

@app.get('/calculate')
def calculate():
    with tracer.start_as_current_span('calculate-sum') as span:
        result = sum(range(1, 101))
        span.set_attribute('calculation.result', result)
        return jsonify(operation='sum(1..100)', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
