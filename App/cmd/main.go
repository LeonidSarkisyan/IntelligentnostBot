package main

import (
	"App/internal/handlers"
	"App/pkg/server"
	"App/pkg/systems"
	"context"
	"os"
	"os/signal"
	"syscall"

	"github.com/rs/zerolog/log"
)

func main() {
	systems.SetupLogger()
	cfg := systems.MustConfig()
	conn := systems.MustConn(cfg)

	handler := handlers.NewHandler(cfg)

	server_ := new(server.Server)

	go func() {
		if err := server_.Run(cfg.Port, handler.InitRoutes()); err != nil {
			log.Fatal().Err(err).Msg("ошибка при запуске сервера")
		}
	}()

	log.Printf("MakeTest старует на порту: %s", cfg.Port)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT)
	<-quit

	log.Print("Сервер остановил свою работу")

	if err := server_.Shutdown(context.Background()); err != nil {
		log.Err(err).Msg("ошибка при остановке сервера")
	}

	if err := conn.Close(); err != nil {
		log.Error().Err(err).Msg("ошибка при закрытии соединения с БД")
	}
}
