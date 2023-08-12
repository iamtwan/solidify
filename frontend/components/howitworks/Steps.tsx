import styles from './howitworks.module.css';

export default function Steps({ title, text }: {
  title: string,
  text: string
}) {
  return <div className={styles['steps-container']}>
    <h6 className={styles['steps-title']}>{title}</h6>
    <p className={styles['steps-text']}>{text}</p>
  </div>
}