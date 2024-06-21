package systems

import (
	"fmt"
	"github.com/joho/godotenv"
	"github.com/rs/zerolog/log"
	"github.com/spf13/viper"
	"os"
)

type AppConfig struct {
	Port    string
	Address string
	Debug   bool

	Database DBConfig

	OpenAIUrl string

	SMTP
}

type SMTP struct {
	Host string
	Port string
}

type DBConfig struct {
	Host string
	Port string
	User string
	Pass string
	Name string
	URL  string
}

func MustConfig() *AppConfig {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal().Msgf("ошибка при подключении env - файла: %s", err.Error())
	}

	viper.AddConfigPath("configs")
	viper.SetConfigName("config")
	err = viper.ReadInConfig()
	if err != nil {
		log.Fatal().Msgf("ошибка при получении конфига: %s", err.Error())
	}

	cfg, err := getConfig()
	if err != nil {
		log.Fatal().Msgf("ошибка при получении конфига: %s", err.Error())
	}

	cfg.Database.URL = fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		cfg.Database.User, cfg.Database.Pass, cfg.Database.Host, cfg.Database.Port, cfg.Database.Name)

	return cfg
}

func getConfig() (*AppConfig, error) {
	cfg := AppConfig{
		Debug:     viper.GetBool("debug"),
		OpenAIUrl: viper.GetString("open_ai_url"),
		SMTP: SMTP{
			Host: viper.GetString("smtp.host"),
			Port: viper.GetString("smtp.port"),
		},
	}

	if cfg.Debug {
		cfg.Address = viper.GetString("local.address")
		cfg.Port = viper.GetString("local.port")

		cfg.Database = DBConfig{
			Host: viper.GetString("test_db.host"),
			Port: viper.GetString("test_db.port"),
			User: viper.GetString("test_db.user"),
			Pass: viper.GetString("test_db.pass"),
			Name: viper.GetString("test_db.name"),
		}
	} else {
		cfg.Address = viper.GetString("prod.address")
		cfg.Port = viper.GetString("prod.port")

		cfg.Database = DBConfig{
			Host: viper.GetString("prod_db.host"),
			Port: viper.GetString("prod_db.port"),
			User: os.Getenv("DB_USER"),
			Pass: os.Getenv("DB_PASS"),
			Name: viper.GetString("prod_db.name"),
		}
	}

	return &cfg, nil
}
