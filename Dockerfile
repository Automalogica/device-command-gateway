# ── Build stage ──────────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN ./mvnw -q -DskipTests package || true
# Placeholder: substituir pelo build real do projeto (Maven/Gradle)


# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jre-alpine

LABEL maintainer="Lucas Nascimento"
LABEL description="Camera Command Agent — MQTT consumer + Telnet executor"

WORKDIR /app

# Cria usuário não-root para execução
RUN addgroup -S agent && adduser -S agent -G agent

# Copia artefato gerado no build
# COPY --from=builder /app/target/camera-agent.jar app.jar

# Para desenvolvimento, permite montar o jar diretamente via volume
# Remover esta linha e descomentar o COPY acima em produção
COPY target/camera-agent.jar app.jar 2>/dev/null || echo "Jar not found, use volume mount"

USER agent

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD wget -qO- http://localhost:8080/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]