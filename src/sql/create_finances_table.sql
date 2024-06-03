-- Table: public.finances

DROP TABLE IF EXISTS public.finances;

CREATE TABLE IF NOT EXISTS public.finances
(
    id serial NOT NULL,
    updatedAt DATE NOT NULL,
    transactType VARCHAR COLLATE pg_catalog."default" NOT NULL,
    amount FLOAT NOT NULL,
    reason VARCHAR COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT financesKey PRIMARY KEY (id)
)

TABLESPACE pg_default;
