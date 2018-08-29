# -*- coding:utf-8 -*-
import sys
import os
import json
import requests
from lxml import etree

class Team:
    def __init__(self, teamId, teamName, location):
        self.teamId = teamId
        self.teamName = teamName
        self.location = location
    def __str__(self):
        return "teamName:{}\tlocation:{}".format(self.teamName, self.location)

class Player:
    def __init__(self, playerBaseInfoObj):
        self.playerId = playerBaseInfoObj['playerId']
        self.teamId = playerBaseInfoObj['teamId']
        self.birthDate = playerBaseInfoObj['birthDate']
        self.cnAlias = playerBaseInfoObj['cnAlias']
        self.cnName = playerBaseInfoObj['cnName']
        self.draftYear = playerBaseInfoObj['draftYear']
        self.enName = playerBaseInfoObj['enName']
        self.height = playerBaseInfoObj['height']
        self.position = playerBaseInfoObj['position']
        self.wage = playerBaseInfoObj['wage']
        self.weight = playerBaseInfoObj['weight']
    def __str__(self):
        return "name:{}\tcnName:{}\tposition:{}\tbrithDate:{}\tdraftYear:{}\theight:{}\tweight:{}\twage:{}".format(self.enName, self.cnName, self.position, self.birthDate, self.draftYear, self.height, self.weight, self.wage)

def getTeamInfos():
    url = 'http://matchweb.sports.qq.com/team/list?columnId=100000&competitionId=100000'
    res = requests.get(url)
    jsonData = res.json()
    teamInfos = []
    eastTeams = jsonData['data']['east']
    for teamObj in eastTeams:
        curTeam = Team(teamObj['teamId'], teamObj['name'], 'east')
        # print(curTeam)
        teamInfos.append(curTeam)
    westTeams = jsonData['data']['west']
    for teamObj in eastTeams:
        curTeam = Team(teamObj['teamId'], teamObj['name'], 'west')
        teamInfos.append(curTeam)
        # print(curTeam)
    return teamInfos

    

def getPlayerInfos(teamInfos, savePath):
    #use to get player ids of a certain team
    urlPrefix = 'http://ziliaoku.sports.qq.com/cube/index?cubeId=10&dimId=31&params=t2:2017|t3:1|t4:'
    urlSuffix = '&from=sportsdatabase'
    #use to get detail player infos of a certain team
    urlPrefix2 = 'http://ziliaoku.sports.qq.com/cube/index?&cubeId=8&dimId=5&params=t1:'
    playerInfos = []
    with open(savePath, 'w') as file:
        for team in teamInfos:
            title = '------------{} {}------------\n'.format(team.teamName, team.location)
            print(title)
            file.write(title)
            url = '{}{}{}'.format(urlPrefix, team.teamId, urlSuffix)
            res = requests.get(url)
            jsonData = res.json()
            playerIds = []
            for playerObj in jsonData['data']['nbaTeamPlayerSeasonStat']:
                playerIds.append(playerObj['playerId'])
            url = '{}{}{}'.format(urlPrefix2, ','.join(playerIds), urlSuffix)
            res = requests.get(url)
            jsonData = res.json()
            for playerObj in jsonData['data']['playerBaseInfo']:
                curPlayer = Player(playerObj)
                playerInfos.append(curPlayer)
                # print(curPlayer)
                file.write('{}\n'.format(curPlayer))
            file.write('\n')

def beginCrawl(savePath):
    teamInfos = getTeamInfos()
    playerInfos = getPlayerInfos(teamInfos, savePath)

if __name__ == '__main__':
    savePath = 'playerInfo.txt'
    beginCrawl(savePath)

