package handlers

import (
	"App/internal/middlewares"
	"App/pkg/systems"

	"github.com/gin-gonic/gin"
)

type Handler struct {
	Config *systems.AppConfig
}

func NewHandler(cfg *systems.AppConfig) *Handler {
	return &Handler{cfg}
}

func (h *Handler) InitRoutes() *gin.Engine {
	router := gin.New()

	router.Use(middlewares.LoggerMiddleware())

	router.LoadHTMLGlob("templates/*")

	router.Static("/static", "./static")

	router.GET("/card", h.CardPage)

	return router
}
