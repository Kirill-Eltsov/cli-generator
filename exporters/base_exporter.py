import json
import csv
import logging
from typing import List, Dict, Any, Optional


logger = logging.getLogger(__name__)


def export_data(data: List[Dict[str, Any]],
                format: str,
                output_file: Optional[str] = None,
                mask_data: bool = False) -> bool:
    """
    Экспортирует данные в указанном формате.

    Args:
        data: Данные для экспорта
        format: Формат экспорта (csv, json, sql)
        output_file: Путь к файлу для сохранения
        mask_data: Нужно ли маскировать чувствительные данные

    Returns:
        bool: Успех операции
    """
    try:
        if mask_data:
            data = _mask_sensitive_data(data)

        if format == 'json':
            return _export_json(data, output_file)
        elif format == 'csv':
            return _export_csv(data, output_file)
        elif format == 'sql':
            return _export_sql(data, output_file)
        else:
            logger.error(f"Неподдерживаемый формат: {format}")
            return False

    except Exception as e:
        logger.error(f"Ошибка при экспорте данных: {e}")
        return False


def _mask_sensitive_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Маскирует чувствительные данные"""
    if not data:
        return data

    def mask_credit_card(card_number: str) -> str:
        """Маскировка номера кредитной карты"""
        card_number = str(card_number).replace(' ', '').replace('-', '')
        if len(card_number) < 10:
            return '*' * len(card_number)
        return card_number[:6] + '*' * (len(card_number) - 10) + card_number[-4:]

    def mask_string(text: str, visible_start: int = 2, visible_end: int = 2) -> str:
        """Общая функция маскировки строки"""
        text = str(text)
        if len(text) <= visible_start + visible_end:
            return '*' * len(text)
        return text[:visible_start] + '*' * (len(text) - visible_start - visible_end) + text[-visible_end:]

    def mask_email(email: str) -> str:
        """Маскировка email адреса"""
        if '@' not in email:
            return mask_string(email, 2, 2)
        local, domain = email.split('@', 1)
        masked_local = mask_string(local, 2, 0)
        masked_domain = mask_string(domain, 1, 1)
        return f"{masked_local}@{masked_domain}"

    def mask_phone(phone: str) -> str:
        """Маскировка номера телефона"""
        phone = str(phone)
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) >= 10:
            return mask_string(digits, 3, 2)
        return mask_string(phone, 2, 2)

    def mask_ip(ip: str) -> str:
        """Маскировка IP адреса"""
        parts = str(ip).split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.***.***"
        return mask_string(ip, 2, 2)

    def mask_uuid(uuid_str: str) -> str:
        """Маскировка UUID"""
        uuid_str = str(uuid_str)
        if len(uuid_str) >= 8:
            return uuid_str[:4] + '****-****-****-' + uuid_str[-4:]
        return mask_string(uuid_str, 2, 2)

    def mask_value(key: str, value: Any) -> Any:
        """Маскирует значение в зависимости от ключа"""
        if value is None:
            return value

        key_lower = key.lower()

        if isinstance(value, dict):
            return {k: mask_value(k, v) for k, v in value.items()}
        elif isinstance(value, list):
            return [mask_value(f"{key}_item", item) for item in value]

        value_str = str(value)

        if 'card' in key_lower and ('number' in key_lower or key_lower == 'card_number'):
            return mask_credit_card(value_str)
        elif 'phone' in key_lower or 'tel' in key_lower:
            return mask_phone(value_str)
        elif 'email' in key_lower or 'mail' in key_lower:
            return mask_email(value_str)
        elif 'ip' in key_lower or 'address' in key_lower and 'source' in key_lower:
            return mask_ip(value_str)
        elif key_lower in ['id', 'uuid']:
            return mask_uuid(value_str)
        elif 'passport' in key_lower or ('series' in key_lower and 'number' in key_lower):
            if 'series' in key_lower:
                return mask_string(value_str, 2, 0)
            elif 'number' in key_lower:
                return mask_string(value_str, 0, 4)
            return mask_string(value_str, 2, 4)
        elif 'inn' in key_lower or 'snils' in key_lower:
            return mask_string(value_str, 4, 4)
        elif 'cvv' in key_lower or 'cvc' in key_lower:
            return '***'
        elif 'password' in key_lower or 'passwd' in key_lower:
            return '********'
        elif 'token' in key_lower or 'secret' in key_lower or 'key' in key_lower:
            return mask_string(value_str, 4, 4)

        return value

    masked_data = []
    for row in data:
        masked_row = {}
        for key, value in row.items():
            masked_row[key] = mask_value(key, value)
        masked_data.append(masked_row)

    logger.info(f"Замаскировано {len(masked_data)} записей")
    return masked_data


def _export_json(data: List[Dict[str, Any]], output_file: Optional[str]) -> bool:
    """Экспорт в JSON"""
    try:
        json_data = json.dumps(data, ensure_ascii=False, indent=2)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
        else:
            print(json_data)

        return True
    except Exception as e:
        logger.error(f"Ошибка при экспорте в JSON: {e}")
        return False


def _export_csv(data: List[Dict[str, Any]], output_file: Optional[str]) -> bool:
    """Экспорт в CSV"""
    try:
        if not data:
            logger.warning("Нет данных для экспорта в CSV")
            return False

        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        fieldnames = sorted(all_keys)

        def process_value(value: Any) -> str:
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False)
            elif value is None:
                return ''
            else:
                return str(value)

        csv_rows = []
        for row in data:
            csv_row = {key: process_value(row.get(key)) for key in fieldnames}
            csv_rows.append(csv_row)

        if output_file:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)
        else:
            import sys
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)

        return True
    except Exception as e:
        logger.error(f"Ошибка при экспорте в CSV: {e}")
        return False


def _export_sql(data: List[Dict[str, Any]], output_file: Optional[str]) -> bool:
    """Экспорт в SQL"""
    try:
        if not data:
            logger.warning("Нет данных для экспорта в SQL")
            return False

        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        fieldnames = sorted(all_keys)
        table_name = "generated_data"

        def get_sql_type(fieldname: str, sample_values: List[Any]) -> str:
            non_null_values = [v for v in sample_values if v is not None]
            if not non_null_values:
                return "TEXT"
            
            sample = non_null_values[0]
            if isinstance(sample, bool):
                return "BOOLEAN"
            elif isinstance(sample, int):
                return "INTEGER"
            elif isinstance(sample, float):
                return "REAL"
            elif isinstance(sample, (dict, list)):
                return "TEXT"
            else:
                max_len = max((len(str(v)) for v in non_null_values), default=255)
                if max_len <= 255:
                    return "VARCHAR(255)"
                elif max_len <= 1000:
                    return "TEXT"
                else:
                    return "TEXT"

        def escape_sql_value(value: Any) -> str:
            if value is None:
                return "NULL"
            elif isinstance(value, bool):
                return "TRUE" if value else "FALSE"
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, (dict, list)):
                json_str = json.dumps(value, ensure_ascii=False)
                escaped = json_str.replace("'", "''")
                return f"'{escaped}'"
            else:
                str_value = str(value)
                escaped = str_value.replace("'", "''")
                return f"'{escaped}'"

        sql_lines = []
        sql_lines.append(f"-- SQL Export: {len(data)} rows")
        sql_lines.append(f"-- Generated table: {table_name}")
        sql_lines.append("")
        sql_lines.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")

        column_definitions = []
        for fieldname in fieldnames:
            sample_values = [row.get(fieldname) for row in data if fieldname in row]
            sql_type = get_sql_type(fieldname, sample_values)
            column_definitions.append(f"    {fieldname} {sql_type}")

        sql_lines.append(",\n".join(column_definitions))
        sql_lines.append(");")
        sql_lines.append("")

        for row in data:
            values = [escape_sql_value(row.get(key)) for key in fieldnames]
            columns_str = ", ".join(fieldnames)
            values_str = ", ".join(values)
            sql_lines.append(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});")

        sql_content = "\n".join(sql_lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sql_content)
        else:
            print(sql_content)

        return True
    except Exception as e:
        logger.error(f"Ошибка при экспорте в SQL: {e}")
        return False
