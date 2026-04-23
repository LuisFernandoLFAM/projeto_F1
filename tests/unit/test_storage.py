"""Testes unitários para o módulo de storage."""

import csv
import tempfile
from pathlib import Path

import pytest

from projeto_f1.models import Lap, Session
from projeto_f1.storage.csv_writer import salvar_csv


class TestSalvarCsv:
    def test_cria_arquivo_csv(self, sessao_corrida):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = salvar_csv([sessao_corrida], "sessoes", diretorio=tmp)
            assert caminho.exists()

    def test_arquivo_tem_cabecalho_correto(self, sessao_corrida):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = salvar_csv([sessao_corrida], "sessoes", diretorio=tmp)
            with open(caminho, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                assert "session_key" in reader.fieldnames
                assert "session_name" in reader.fieldnames

    def test_adiciona_extensao_csv(self, sessao_corrida):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = salvar_csv([sessao_corrida], "sessoes_sem_extensao", diretorio=tmp)
            assert caminho.suffix == ".csv"

    def test_nao_duplica_extensao_csv(self, sessao_corrida):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = salvar_csv([sessao_corrida], "sessoes.csv", diretorio=tmp)
            assert caminho.name == "sessoes.csv"

    def test_lista_vazia_lanca_value_error(self):
        with pytest.raises(ValueError, match="não pode ser vazia"):
            salvar_csv([], "arquivo")

    def test_quantidade_de_linhas_corretas(self, lista_voltas):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = salvar_csv(lista_voltas, "voltas", diretorio=tmp)
            with open(caminho, encoding="utf-8") as f:
                linhas = list(csv.DictReader(f))
            assert len(linhas) == len(lista_voltas)

    def test_retorna_path(self, sessao_corrida):
        with tempfile.TemporaryDirectory() as tmp:
            resultado = salvar_csv([sessao_corrida], "teste", diretorio=tmp)
            assert isinstance(resultado, Path)
