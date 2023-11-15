CREATE TABLE "player_data" (
    "player_id" varchar(30)   NOT NULL,
    "player_name" varchar(30)   NOT NULL,
    "team_id" varchar(30)   NOT NULL,
    "position_id" varchar(30)   NOT NULL,
    "jersey_number" int   NOT NULL,
    "goals" int   NOT NULL,
    "assists" int   NOT NULL,
    "yellow_cards" int   NOT NULL,
    "red_cards" int   NOT NULL,
    "shots" int   NOT NULL,
    "shots_on_goal" int   NOT NULL,
    "saves" int   NOT NULL,
    "clean_sheets" int   NOT NULL,
    "goals_against" int   NOT NULL,
    "photo_url" varchar(500)   NOT NULL,
    "height" float   NOT NULL,
    "weight" int   NOT NULL,
    "birthdate" date   NOT NULL,
    "nationality_id" varchar(30)   NOT NULL,
    CONSTRAINT "pk_Player_Data" PRIMARY KEY (
        "player_id"
     )
);

CREATE TABLE "league" (
    "league_id" varchar(30)   NOT NULL,
    "league" varchar(30)   NOT NULL,
    CONSTRAINT "pk_Leagues" PRIMARY KEY (
        "league_id"
     )
);

CREATE TABLE "team" (
    "team_id" varchar(30)   NOT NULL,
    "team" varchar(30)   NOT NULL,
    "league_id" varchar(30)   NOT NULL,
    CONSTRAINT "pk_Teams" PRIMARY KEY (
        "team_id"
     )
);

CREATE TABLE "position" (
    "position_id" varchar(30)   NOT NULL,
    "position" varchar(30)   NOT NULL,
    CONSTRAINT "pk_Positions" PRIMARY KEY (
        "position_id"
     )
);

CREATE TABLE "nationality" (
    "nationality_id" varchar(30)   NOT NULL,
    "nationality" varchar(30)   NOT NULL,
    CONSTRAINT "pk_Nationalities" PRIMARY KEY (
        "nationality_id"
     )
);

ALTER TABLE "player_data" ADD CONSTRAINT "fk_player_data_team_id" FOREIGN KEY("team_id")
REFERENCES "team" ("team_id");

ALTER TABLE "player_data" ADD CONSTRAINT "fk_player_data_position_id" FOREIGN KEY("position_id")
REFERENCES "position" ("position_id");

ALTER TABLE "player_data" ADD CONSTRAINT "fk_player_data_nationality_id" FOREIGN KEY("nationality_id")
REFERENCES "nationality" ("nationality_id");

ALTER TABLE "team" ADD CONSTRAINT "fk_team_league_id" FOREIGN KEY("league_id")
REFERENCES "league" ("league_id");

