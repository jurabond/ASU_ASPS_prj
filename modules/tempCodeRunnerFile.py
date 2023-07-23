      to = "engineer@example.com"  # Email інженера
        subject = "Виклик інженера"
        body = f"Виклик інженера від користувача: {self.username}"
        send_email(to, subject, body)
        station_id = "0"  # Замініть на потрібне значення для відповідної станції
        event_module.add_event("Виклик інженера", station_id)