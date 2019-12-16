import React from 'react';
import { Grid, Paper, Typography, IconButton, TextField, CardActions, Card,
CardHeader, CardContent, Input, Modal, Button, Tooltip } from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import SearchIcon from '@material-ui/icons/Search';
import HelpIcon from '@material-ui/icons/Help';
import useStyle from './classes';
import './App.css';
import api from './services/api';

const Elixir = require('./media/Elixir.png')

const cls = (...item) => item.join(' ')
const parseText = (text) => text.toLowerCase().split('-').join(' ').split('.').join(' ')
const makeImgName = (name) => parseText(name).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/(?:^|\s)\S/g, e => e.toUpperCase()).split(' ').join('');

function App() {
  const classes = useStyle();
  const [open, setOpen] = React.useState(false);
  const [cartas, setCartas] = React.useState([
    {nome: 'Cura', custo:1},
    {nome: 'Espelho', custo:3},
    {nome: 'Espírito de Gelo', custo:1},
    {nome: 'Esqueletos', custo:1},
    {nome: 'Bola de Neve', custo:2},
    {nome: 'Destruidores de Muros', custo:2},
    {nome: 'Morcegos', custo:2},
    {nome: 'Barril de Bárbaro', custo:2},
    {nome: 'Fúria', custo:2},
    {nome: 'Espíritos de Fogo', custo:2},
    {nome: 'Goblins', custo:2},
    {nome: 'Goblins Lanceiros', custo:2},
    {nome: 'Terremoto', custo:3},
    {nome: 'Servos', custo:3},
    {nome: 'Arqueiras', custo:3},
    {nome: 'Clone', custo:3},
    {nome: 'Barril de Esqueletos', custo:3},
    {nome: 'Tornado', custo:3},
    {nome: 'Mago de Gelo', custo:3},
    {nome: 'Canhão', custo:3},
    {nome: 'Guardas', custo:3},
    {nome: 'Fantasma Real', custo:3},
    {nome: 'Lápide', custo:3},
    {nome: 'Bandida', custo:3},
    {nome: 'Barril de Goblin', custo:3},
    {nome: 'Bombardeiro', custo:3},
    {nome: 'Mineiro', custo:3},
    {nome: 'Gangue de Goblins', custo:3},
    {nome: 'Flechas', custo:3},
    {nome: 'Goblin com Dardo', custo:3},
    {nome: 'Megasservo', custo:3},
    {nome: 'Golem de Elixir', custo:3},
    {nome: 'Dragão Infernal', custo:4},
    {nome: 'Aríete de Batalha', custo:4},
    {nome: 'Lenhador', custo:4},
    {nome: 'Valquíria', custo:4},
    {nome: 'Bola de Fogo', custo:4},
    {nome: 'Caçador', custo:4},
    {nome: 'Jaula de Goblin', custo:4},
    {nome: 'Gelo', custo:4},
    {nome: 'Fornalha', custo:4},
    {nome: 'Mosqueteira', custo:4},
    {nome: 'Príncipe das Trevas', custo:4},
    {nome: 'Tesla', custo:4},
    {nome: 'Eletrocutadores', custo:4},
    {nome: 'Torre de Bombas', custo:4},
    {nome: 'Morteiro', custo:4},
    {nome: 'Veneno', custo:4},
    {nome: 'Corredor', custo:4},
    {nome: 'Máquina Voadora', custo:4},
    {nome: 'Bebê Dragão', custo:4},
    {nome: 'Mini P.E.K.K.A', custo:4},
    {nome: 'Bruxa', custo:5},
    {nome: 'Dragão Elétrico', custo:5},
    {nome: 'Porcos Reais', custo:5},
    {nome: 'Cabana de Goblins', custo:5},
    {nome: 'Carrinho de Canhão', custo:5},
    {nome: 'Torre Inferno', custo:5},
    {nome: 'Patifes', custo:5},
    {nome: 'Balão', custo:5},
    {nome: 'Executor', custo:5},
    {nome: 'Lançador', custo:5},
    {nome: 'Gigante', custo:5},
    {nome: 'Cemitério', custo:5},
    {nome: 'Horda de Servos', custo:5},
    {nome: 'Príncipe', custo:5},
    {nome: 'Bárbaros', custo:5},
    {nome: 'Domadora de Carneiro', custo:5},
    {nome: 'Goblin Gigante', custo:6},
    {nome: 'Coletor de Elixir', custo:6},
    {nome: 'X-Besta', custo:6},
    {nome: 'Gigante Real', custo:6},
    {nome: 'Esqueleto Gigante', custo:6},
    {nome: 'Megacavaleiro', custo:7},
    {nome: 'Cabana de Bárbaros', custo:7},
    {nome: 'Recrutas Reais', custo:7},
    {nome: 'Lava Hound', custo:7},
    {nome: 'Golem', custo:8},
    {nome: 'Três Mosqueteiras', custo:9},
    {nome: 'Pescador', custo:3},
    {nome: 'Bruxa Sombria', custo:4},
    {nome: 'Arqueiro Mágico', custo:4},
    {nome: 'P.E.K.K.A', custo:7},
    {nome: 'Mago', custo:5},
    {nome: 'Cavaleiro', custo:3},
    {nome: 'O Tronco', custo:2},
    {nome: 'Exército de Esqueletos', custo:3},
    {nome: 'Princesa', custo:3},
    {nome: 'Mago Elétrico', custo:4},
    {nome: 'Zap', custo:2}
  ].map(e => ({...e, img: require(`./media/cards/${makeImgName(e.nome)}Card.png`)})));
  const [currentDeck, setCurrentDeck] = React.useState({
    cartas: Array(8).fill(null)
  });
  const [currentCard, setCurrentCard] = React.useState(null);
  const [isEditing, setIsEditing] = React.useState(false);
  const rootRef = React.useRef(null);
  
  const handleSelect = i => e => {
    e.preventDefault();
    setOpen(true);
    setCurrentCard(i);
  }

  const handleChange = tipo => e => {
    const target = e.target;
    setCurrentDeck(old => ({...old, [tipo]: target.value}));
  }

  const handleCardSelect = card => e => {
    e.preventDefault();
    setOpen(false);
    setCurrentDeck(old => {
      old.cartas[currentCard] = card;
      return old;
    })
    setCartas(old => {
      if (currentDeck.cartas[currentCard]) {
        return [...old, currentDeck.cartas[currentCard]].map(e => e != card ? e : null)
      } else {
        return old.map(e => e != card ? e : null)  
      }
    });
  }

  const deck = (deckData) => {
    return (
      <Grid item md={6}>
        <Card className={classes.card}>
          <CardHeader
            title={<Typography variant="body1" className={classes.deckTitle}>{`${deckData.nome}#${deckData.codigo}`}</Typography>}
            // subheader={<Typography variant="subtitle2">September 14, 2016</Typography>}
            className={classes.cardHeader}
            action={
              <Tooltip title={
              <div>
                <p>{deckData.descricao}</p>
                <p>{deckData.data_criacao}</p>
              </div>}
              style={{marginRight: '10px', marginTop: '10px'}}>
                <HelpIcon className={classes.icon}/>
              </Tooltip>
            }
          />
          <CardContent className={classes.cardContent}>
            <Grid container spacing={2}>
              {deckData.cartas.map(carta => (
                <Grid item md={3}>
                  <img
                      className={classes.carta}
                      src={require(`./media/cards/${makeImgName(carta.carta_nome)}Card.png`)}
                      title={carta.carta_nome}
                    />
                </Grid>
              ))}
            </Grid>
          </CardContent>
          <CardActions disableSpacing className={classes.cardFoot}>
            <div style={{
              display: 'flex',
              alignItems: 'inherit',
              justifyContent: 'inherit'
            }}>
              <IconButton size='small'>
                <img alt='Elixir' src={Elixir} style={{height: '24px'}} />
              </IconButton>
              <Typography className={classes.deckTitle}>
                <strong>{deckData.custo}</strong>
              </Typography>
            </div>
            <div>
              <IconButton size='small' className={classes.icon} onClick={() => {
                setCurrentDeck({
                  ...deckData,
                  cartas: Array(8).fill(null).map((e, i) => deckData.cartas[i] ? deckData.cartas[i] : null)
                });
                setIsEditing(true);
              }}>
                <EditIcon />
              </IconButton>
              <IconButton size='small' className={classes.icon} onClick={() => handleDelete(deckData.codigo)}>
                <DeleteIcon />
              </IconButton>
            </div>
          </CardActions>
        </Card>
      </Grid>
    );
  }

  function saveDeck(e) {
    e.preventDefault();
    setIsEditing(false);
    const cartas = currentDeck.cartas.filter(v => v !== null);
    const custo = Math.round(10 * cartas.map(carta => carta.custo).reduce((a, b) => a + b,0) / cartas.length) / 10;
    const data = new Date().toISOString().substring(0, 10);
    api.post(`/add_deck?descricao=${currentDeck.descricao}&nome=${currentDeck.nome}&custo=${custo}&data_criacao=${data}&cartas=${JSON.stringify(cartas.map(v => ({nome: v.nome})))}`)
    .then(v => {
      alert('Deck salvo com Sucesso!')
    })
    .catch(error => {
      alert('Não foi possível salvar o Deck!')
    })
  }

  function updateDeck(e) {
    e.preventDefault();
    const cartas = currentDeck.cartas.filter(v => v !== null);
    const custo = Math.round(10 * cartas.map(carta => carta.custo).reduce((a, b) => a + b,0) / cartas.length) / 10;
    const data = new Date().toISOString().substring(0, 10);
    api.post(`/update_deck?codigo_deck=${currentDeck.codigo_deck}&descricao=${currentDeck.descricao}&nome=${currentDeck.nome}&custo=${custo}&data_criacao=${data}&cartas=${JSON.stringify(cartas.map(v => ({nome: v.nome})))}`)
    .then(v => {
      alert('Deck salvo com Sucesso!')
    })
    .catch(error => {
      alert('Não foi possível salvar o Deck!')
    })
  }

  const handleDelete = codigo => (e) => {
    e.preventDefault();
    api.post(`/remove_deck?codigo_deck=${codigo}`)
    .then(v => {
      alert('Deck deletado com Sucesso')
    })
    .catch(error => {
      alert('Não foi possível excluir o Deck!')
    })
  }

  React.useEffect(() => {
    // api.get('/list_cartas').then(res => {
    //   const data = res.data;
    //   setCartas(Object.values(data).map(e => ({...e, img: require(`./media/cards/${makeImgName(e.nsome)}Card.png`)})));
    // });
  }, [])

  return (
    <div className={classes.h100}>
      <Grid container className={classes.h100}>
        <Grid item lg={6} className={cls(classes.grid, classes.h100)}>
          <Paper className={classes.paper} style={{height: 'calc(100% - 32px)'}}>
            <Typography style={{marginBottom: '16px'}} variant="h4"><strong>Clash Royale Deck Manager</strong></Typography>
            <TextField style={{marginBottom: '16px'}} label="Nome do Deck" variant="outlined" fullWidth inputProps={{ maxLength: 50 }} onChange={handleChange('nome')} value={currentDeck.nome ? currentDeck.nome : ''}/>
            <TextField label="Descrição" variant="outlined" fullWidth inputProps={{ maxLength: 200 }} multiline rowsMax={3} onChange={handleChange('descricao')} value={currentDeck.descricao ? currentDeck.descricao : ''}/>
            <center>  
              <Grid container spacing={2} style={{width: '90%', margin: '20px 0'}}>
                {currentDeck.cartas.map((e, i) => (
                  <Grid item md={3}>
                    <Paper className={classes.largeZone} onClick={handleSelect(i)}>
                      {e && (
                        <img
                          className={classes.h100}
                          src={e.img}
                          title={e.nome}
                        />
                      )}
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </center>
            <div style={{float: 'right'}}>
              {isEditing && <Button variant='outlined' color='primary' onClick={updateDeck}>Atualizar</Button>}
              {' '}
              <Button variant='contained' color='primary' onClick={saveDeck}>Salvar novo</Button>
            </div>
          </Paper>
        </Grid>
        <Grid item lg={6} className={cls(classes.grid, classes.left, classes.h100)}>
          <Paper className={classes.paper} style={{marginBottom: '16px'}}>
            <Grid container spacing={1} alignItems="flex-end">
              <Grid item>
                <SearchIcon />
              </Grid>
              <Grid item className={classes.wFill}>
                <Input placeholder="Pesquisar" fullWidth />
              </Grid>
            </Grid>
          </Paper>
          <Grid container spacing={2}>
            {deck({
              codigo: 1,
              nome: 'Deck de P.E.K.K.A',
              descricao: 'Deck forte de P.E.K.K.A',
              custo: 3.6,
              data_criacao: '2019-12-15',
              cartas: [{...cartas[3], carta_nome: 'Cavaleiro'}]
            })}
          </Grid>
        </Grid>
      </Grid>

      <Modal
        disablePortal
        disableEnforceFocus
        disableAutoFocus
        open={open}
        className={classes.modal}
        container={() => rootRef.current}
      >
        <div className={classes.paper_modal}>
          <div>
            <Typography className={classes.modalTitle} variant='h5'>Escolha uma carta</Typography>
            <Button variant='contained' color='secondary' className={classes.modalCancelBtn} onClick={() => setOpen(false)}>Cancelar</Button>
          </div>
          <Grid container spacing={1}>
            {cartas.map((e, i) => (
              e ? (
                <Grid item md={2} key={i}>
                  <div style={{position: 'relative'}}>
                    <img
                      src={e.img}
                      alt={e.nome}
                      title={e.nome}
                      className={classes.w100}
                      style={{cursor: 'pointer'}}
                      onClick={handleCardSelect(e)}
                    />
                    <img src={Elixir} alt='Elixir' className={classes.elixirBadge} />
                    <p className={classes.elixirCusto}>{e.custo}</p>
                  </div>
                </Grid>
              ) : null
            ))}
          </Grid>
        </div>
      </Modal>
    </div>
  );
}

export default App;
