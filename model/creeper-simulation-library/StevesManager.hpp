#pragma once

#include <list>
#include <vector>

#include "Steve.hpp"

class Simulation;
/**
 * @class StevesManager
 * @brief Менеджер для управления сущностями типа Steve.
 *
 * Класс StevesManager предоставляет функциональность для хранения, доступа и управления
 * объектами типа Steve. Включает методы для выполнения действий, таких как перемещение.
 */
class StevesManager {
  std::shared_ptr<StevesParams> params_;
  std::vector<std::shared_ptr<Steve>> steves_;

 protected:
 /**
  * @brief Получает ссылку на коллекцию объектов Steve.
  * @return Ссылка на вектор объектов Steve.
  */
  [[nodiscard]] decltype(steves_)& getStevesRef() { return steves_; }

 public:
 /**
  * @brief Конструктор класса StevesManager.
  * @param params Указатель на параметры, связанные с объектами Steve.
  */
  StevesManager(std::shared_ptr<StevesParams> params);
 /**
  * @brief Возвращает константную ссылку на коллекцию объектов Steve.
  * @return Константная ссылка на вектор объектов Steve.
  */
  [[nodiscard]] const decltype(steves_)& getSteves() const { return steves_; }
 /**
  * @brief Выполняет действие перемещения для всех объектов Steve.
  */
  void walk();

  friend class Simulation;
};
