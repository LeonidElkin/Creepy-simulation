# Creepy-simulation

## Get Started

1. В коммандной строке напишите `poetry install`, чтобы подключить все необходимые зависимости
2. Далее напишите `poetry build`, чтобы сбилдить проект
3. Далее снова `poetry install`, чтобы подключить pybind модуль
4. Можете запускать '  view/view.py`

## Description

Creepy-simulation представляет поле, населенное криперами. Криперы могут взорваться, если подойдут достаточно близко к другому криперу, либо могут начать шипеть, если находятся подальше.

Все криперы при рождении находятся в состоянии `born` и являются неуязвимыми, он выйдет из этого состояния, когда впервые подвигается. Если крипер долго слоняется без дела, он может заснуть, он выйдет из этого состояния, если кто-то заставит его взорваться или начать шипеть. Когда крипер взрывается, он умирает и рождается заново в случайном месте на поле, он также будет в состоянии `born`. Крипер шипит с вероятностью обратной квадрату расстояния между каким-то крипером, он перестанет шипеть, если вероятность не выпадет снова на следующем обновлении.

## Additional features

В данном проекте реализованы следующие дополнительные фичи:
- Использованы различные функции состояния: Евклидово, в полярных координатах, манхэттенское
- Криперы имеют три уникальных состояния: `born`, `sleep`, `explode`
- Логгируются взаимодействия криперов
- Плавная и красивая отрисовка

## Example
