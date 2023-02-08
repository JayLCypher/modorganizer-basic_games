#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pathlib

import PyQt6.QtCore as QtCore
import mobase

from ..basic_game import BasicGame, BasicGameSaveGame

class VampireModDataChecker(mobase.ModDataChecker):
	def __init__(self):
		super().__init__()
		self.validDirNames = [
			"cfg",
			"cl_dlls",
			"dlg",
			"dlls",
			"maps",
			"materials",
			"media",
			"models",
			"particles",
			"python",
			"resource",
			"SAVE",
			"scripts",
			"sound",
			"vdata",
		]

	def dataLooksValid(self, filetree: mobase.IFileTree) -> mobase.ModDataChecker.CheckReturn:
		for entry in filetree:
			if not entry.isDir(): continue
			if entry.name().casefold() in self.validDirNames: return mobase.ModDataChecker.VALID
		return mobase.ModDataChecker.INVALID

class VampireModDataContent(mobase.ModDataContent):
	def __init__(self):
		super().__init__()

class VampireSaveGame(BasicGameSaveGame):
	def __init__(self, filepath: pathlib.Path):
		super().__init__(filepath)

class VampireLocalSavegames(mobase.LocalSavegames):
	def __init__(self, myGameSaveDir: QtCore.QDir):
		super().__init__()
		self._savesDir = myGameSaveDir.absolutePath()

	def mappings(self, profile_save_dir: QtCore.QDir): return [mobase.Mapping(
			source=profile_save_dir.absolutePath(),
			destination=self._savesDir,
			is_directory=True,
			create_target=True
		)]

	def prepareProfile(self, profile):
		return profile.localSavesEnabled()

class VampireTheMasqueradeBloodlinesGame(BasicGame):
	Name = "Vampire - The Masquerade: Bloodlines Support Plugin"
	Author = "John"
	Version = "1.0.0"
	Description = "Adds Mod Organizer 2 version 2.5.0 Basic Game support for Vampires: The Masquerade - Bloodlines"

	GameName = "Vampire The Masquerade - Bloodlines"
	GameShortName = "vampirebloodlines"
	GameNexusName = "vampirebloodlines"
	GameNexusId = 437
	GameSteamId = [2600]
	GameGogId = [1207659240]
	GameBinary = "vampire.exe"
	GameDataPath = "vampire"
	GameDocumentsDirectory = "%GAME_PATH%/vampire/cfg"
	GameSavesDirectory = "%GAME_PATH%/vampire/SAVE"
	GameSaveExtension = "sav"
	GameSupportURL = (
		r"https://github.com/ModOrganizer2/modorganizer-basic_games/wiki/"
		"Game:-Vampire:-The-Masquerade-%E2%80%90-Bloodlines"
	)

	GameTrueName = "Vampire: The Masquerade - Bloodlines"

	def init(self, organizer: mobase.IOrganizer) -> bool:
		super().init(organizer)
		self._featureMap[mobase.ModDataChecker] = VampireModDataChecker()
		self._featureMap[mobase.ISaveGame] = VampireSaveGame(pathlib.Path(self.savesDirectory().absolutePath()))
		self._featureMap[mobase.LocalSavegames] = VampireLocalSavegames(self.savesDirectory())
		return True

	def iniFiles(self):
		return ["autoexec.cfg", "user.cfg"]

	def executables(self) -> list[mobase.ExecutableInfo]:
		execs = []
		if self.getLauncherName():
			execs.append(
				mobase.ExecutableInfo(
					self.GameTrueName,
					QtCore.QFileInfo(self.gameDirectory().absoluteFilePath(self.getLauncherName())),
				)
			)
		execs.append(
			mobase.ExecutableInfo(
				self.GameTrueName,
				QtCore.QFileInfo(self.gameDirectory().absoluteFilePath(self.binaryName())),
			)
		)
		return execs
