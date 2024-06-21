package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func (h *Handler) CardPage(c *gin.Context) {
	c.HTML(http.StatusOK, "card.html", gin.H{})
}
