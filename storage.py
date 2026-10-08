import json
import os
from datetime import date, datetime
from pathlib import Path


class Storage:

    def __init__(self, file_path: Path):

        self.file_path = file_path

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():

            self._create_empty_file()

        self.data = self._load()


    def _create_empty_file(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                ensure_ascii=False,
                indent=4
            )


    def _load(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

        except (
            json.JSONDecodeError,
            OSError
        ):

            return {}


    def _write_file(self):

        temporary_file = self.file_path.with_suffix(
            ".tmp"
        )

        try:

            with open(
                temporary_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

                file.flush()

                os.fsync(
                    file.fileno()
                )

            os.replace(
                temporary_file,
                self.file_path
            )

        except Exception:

            if temporary_file.exists():

                try:
                    temporary_file.unlink()
                except OSError:
                    pass

            raise


    def get_today_value(self):

        key = date.today().isoformat()

        entry = self.data.get(key)

        if isinstance(entry, dict):

            try:
                return int(entry.get("value",0))

            except (TypeError,ValueError):
                return 0

        try:
            return int(entry)

        except (TypeError,ValueError):
            return 0


    def save_today(self, value):

        key = date.today().isoformat()

        now = datetime.now()

        self.data[key] = {
            "value": int(value),
            "saved_at": now.isoformat(
                timespec="minutes"
            )
        }
        self._write_file()


    def get_history(self):

        result = []

        for key, entry in self.data.items():
            try:
                parsed_date = datetime.strptime(
                    key,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                continue

            if isinstance(entry, dict):
                try:
                    value = int( entry.get("value",0))

                except (TypeError,ValueError
                ):
                    value = 0
                saved_at_string = entry.get(
                    "saved_at"
                )

                if saved_at_string:

                    try:
                        saved_at = datetime.fromisoformat(saved_at_string)

                    except ValueError:
                        saved_at = datetime.combine(
                            parsed_date,
                            datetime.min.time()
                        )

                else:

                    saved_at = datetime.combine(
                        parsed_date,
                        datetime.min.time()
                    )

            else:
                try:
                    value = int(entry)
                except (TypeError,ValueError):
                    value = 0
                saved_at = datetime.combine(
                    parsed_date,
                    datetime.min.time()
                )

            result.append(
                {
                    "date": parsed_date,
                    "value": value,
                    "saved_at": saved_at
                }
            )
        result.sort(
            key=lambda item: item["saved_at"],
            reverse=True
        )
        return result


    def delete_date(self, target_date):
        key = target_date.isoformat()
        if key not in self.data:
            return False
        del self.data[key]
        self._write_file()
        return True

    def get_window_position(self):
        entry = self.data.get("__window__")
        if isinstance(entry, dict):
            x = entry.get("x")
            y = entry.get("y")
            if x is None or y is None:
                return None
            try:
                return int(x), int(y)
            except (TypeError, ValueError):
                return None
        return None

    def save_window_position(self, x, y):
        entry = self.data.get("__window__")
        if not isinstance(entry, dict):
            entry = {}
        entry["x"] = int(x)
        entry["y"] = int(y)
        self.data["__window__"] = entry
        self._write_file()

    def get_pinned(self):
        entry = self.data.get("__window__")
        if isinstance(entry, dict):
            return bool(entry.get("pinned", False))
        return False

    def save_pinned(self, pinned):
        entry = self.data.get("__window__")
        if not isinstance(entry, dict):
            entry = {}
        entry["pinned"] = bool(pinned)
        self.data["__window__"] = entry
        self._write_file()